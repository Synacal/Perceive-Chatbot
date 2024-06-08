# import psycopg2
# import logging
# import concurrent.futures

# # Configure logging
# logging.basicConfig(
#     filename="eu_patents_log.txt",
#     level=logging.INFO,
#     format="%(asctime)s - %(message)s",
# )


# def get_all_columns(conn, schema_name, table_name):
#     with conn.cursor() as cur:
#         query = """
#         SELECT column_name
#         FROM information_schema.columns
#         WHERE table_name = %s AND table_schema = %s
#         ORDER BY ordinal_position;
#         """
#         cur.execute(query, (table_name, schema_name))
#         columns = cur.fetchall()
#         return [col[0] for col in columns]


# def load_ids_to_temp_table(conn, file_path):
#     with conn.cursor() as cur:
#         # Create a temporary table
#         cur.execute(
#             """
#         CREATE TEMP TABLE temp_ids (
#             id TEXT
#         );
#         """
#         )

#         # Load data from the text file into the temporary table
#         with open(file_path, "r") as f:
#             cur.copy_expert("COPY temp_ids (id) FROM STDIN WITH (FORMAT text)", f)
#         conn.commit()


# def create_eu_patents_table(conn):
#     with conn.cursor() as cur:
#         # Create the eu_patents table if it does not exist
#         create_table_query = """
#         DO $$
#         BEGIN
#             IF NOT EXISTS (SELECT FROM information_schema.tables
#                            WHERE table_name = 'eu_patents' AND table_schema = 'public') THEN
#                 CREATE TABLE eu_patents AS TABLE target.patents WITH NO DATA;
#             END IF;
#         END $$;
#         """
#         cur.execute(create_table_query)
#         conn.commit()


# def process_batch(batch_num, batch_size, columns, conn_params):
#     try:
#         conn = psycopg2.connect(**conn_params)
#         with conn.cursor() as cur:
#             columns_str = ", ".join(columns)

#             insert_query = f"""
#             INSERT INTO eu_patents ({columns_str})
#             SELECT {columns_str}
#             FROM target.patents
#             WHERE id IN (SELECT id FROM temp_ids LIMIT {batch_size} OFFSET {batch_num * batch_size})
#             RETURNING id;
#             """
#             cur.execute(insert_query)
#             new_records = cur.fetchall()
#             conn.commit()

#             # Log the new records
#             logging.info(f"Batch {batch_num + 1}: {len(new_records)} records added.")
#             for record in new_records:
#                 logging.info(record)

#             delete_query = f"""
#             DELETE FROM target.patents
#             WHERE id IN (SELECT id FROM temp_ids LIMIT {batch_size} OFFSET {batch_num * batch_size});
#             """
#             cur.execute(delete_query)
#             conn.commit()

#             # Remove processed IDs from temp_ids
#             cur.execute(
#                 f"DELETE FROM temp_ids WHERE id IN (SELECT id FROM temp_ids LIMIT {batch_size} OFFSET {batch_num * batch_size});"
#             )
#             conn.commit()

#             print(f"Batch {batch_num + 1} completed.")
#     except Exception as e:
#         logging.error(f"Batch {batch_num + 1} error: {e}")
#     finally:
#         if conn:
#             conn.close()


# def move_patents_in_batches_parallel(conn, columns, batch_size):
#     with conn.cursor() as cur:
#         total_count_query = "SELECT COUNT(*) FROM temp_ids;"
#         cur.execute(total_count_query)
#         total_count = cur.fetchone()[0]
#         batches = (total_count // batch_size) + (
#             1 if total_count % batch_size != 0 else 0
#         )

#     conn_params = {
#         "dbname": conn.info.dbname,
#         "user": conn.info.user,
#         "password": conn.info.password,
#         "host": conn.info.host,
#         "port": conn.info.port,
#     }

#     with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
#         futures = [
#             executor.submit(process_batch, batch_num, batch_size, columns, conn_params)
#             for batch_num in range(batches)
#         ]
#         for future in concurrent.futures.as_completed(futures):
#             future.result()


# def main():
#     # Database connection details
#     dbname = "postgres"
#     user = "ryan"
#     password = "testgpt"
#     host = "percievedb.postgres.database.azure.com"
#     port = "your_port"
#     file_path = "Completed EPO Patent ID List.txt"
#     batch_size = 1000

#     try:
#         # Connect to the PostgreSQL database
#         conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host)

#         # Create the eu_patents table if it does not exist
#         create_eu_patents_table(conn)

#         # Get all columns from the target.patents table
#         columns = get_all_columns(conn, "target", "patents")

#         # Load IDs to temporary table
#         load_ids_to_temp_table(conn, file_path)

#         # Move patents and log new records in parallel batches
#         move_patents_in_batches_parallel(conn, columns, batch_size)

#     except Exception as e:
#         logging.error(f"Error: {e}")

#     finally:
#         if conn:
#             conn.close()


# if __name__ == "__main__":
#     main()
import psycopg2
from psycopg2 import sql


def transfer_ep_patents_batch(batch_size=1000):
    print("Establishing connection to the PostgreSQL database...")
    # Establish connection to the PostgreSQL database
    conn = psycopg2.connect(
        dbname="postgres",
        user="ryan",
        password="testgpt",
        host="percievedb.postgres.database.azure.com",
    )
    cur = conn.cursor()
    print("Connection established.")

    print("Creating target.eu_patents table if it does not exist...")
    # Create the target.eu_patents table if it does not exist
    create_table_query = """
    CREATE TABLE IF NOT EXISTS target.eu_patents AS
    TABLE target.patents WITH NO DATA;
    """
    cur.execute(create_table_query)
    conn.commit()
    print("Table created or already exists.")

    # Select and transfer records in batches
    while True:
        print(f"Selecting up to {batch_size} records starting with 'EP'...")
        # Select records starting with 'EP'
        select_query = sql.SQL(
            """
        SELECT id
        FROM target.patents
        WHERE id LIKE 'EP%'
        LIMIT {}
        """
        ).format(sql.Literal(batch_size))

        cur.execute(select_query)
        ep_patents = cur.fetchall()

        if not ep_patents:
            print("No more records to transfer. Exiting loop.")
            break  # Exit loop if no more records to transfer

        ep_ids = [row[0] for row in ep_patents]
        print(f"Selected {len(ep_ids)} records.")

        # Insert records into target.eu_patents
        print("Inserting selected records into target.eu_patents...")
        insert_query = sql.SQL(
            """
        INSERT INTO target.eu_patents
        SELECT *
        FROM target.patents
        WHERE id = ANY(%s)
        """
        )
        cur.execute(insert_query, (ep_ids,))
        print("Records inserted.")

        # Delete records from target.patents
        print("Deleting inserted records from target.patents...")
        delete_query = sql.SQL(
            """
        DELETE FROM target.patents
        WHERE id = ANY(%s)
        """
        )
        cur.execute(delete_query, (ep_ids,))
        print("Records deleted.")

        # Commit the transaction
        conn.commit()
        print("Transaction committed.")

        # Log transferred IDs
        with open("transferred_ep_ids.txt", "a") as log_file:
            for ep_id in ep_ids:
                log_file.write(f"{ep_id}\n")
        print(f"Transferred IDs logged ({len(ep_ids)} records).")

    # Close the cursor and connection
    cur.close()
    conn.close()
    print("Cursor and connection closed. Batch transfer completed.")


# Example usage
transfer_ep_patents_batch(batch_size=1000)
