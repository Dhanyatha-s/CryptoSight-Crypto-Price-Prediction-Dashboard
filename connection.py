from sqlalchemy import create_engine
from snowflake.sqlalchemy import URL

# snowflake connection 
SNOWFLAKE_USER = "dhanya"
SNOWFLAKE_PASSWORD = "RamaSitaSahitaHanuma@8"
SNOWFLAKE_ACCOUNT = "oiaqyhv-ks32138"
SNOWFLAKE_WAREHOUSE = "cypto_warehouse"
SNOWFLAKE_DATABASE = "crypto_db"
SNOWFLAKE_SCHEMA = "crypto_star_schema"


snowflake_url = URL(
    account = SNOWFLAKE_ACCOUNT,
    user = SNOWFLAKE_USER,
    password = SNOWFLAKE_PASSWORD,
    warehouse = SNOWFLAKE_WAREHOUSE,
    database = SNOWFLAKE_DATABASE,
    schema = SNOWFLAKE_SCHEMA
)

# create engine
engine = create_engine(snowflake_url)

# Test connection
try:
    with engine.connect() as conn:
        print("Successfully connected to Snowflake")
except Exception as e:
    print("Connection failed")