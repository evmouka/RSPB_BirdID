import pandas as pd
import sqlite3
import os
from pathlib import Path

class BirdKnowledgeSetup:
    def __init__(self, db_name: str = "bird_knowledge.db"):
        self.db_name = db_name
        self.conn = None
        self.cursor = None
        
    def connect_db(self):
        """Create and connect to SQLite database"""
        db_path = os.path.abspath(self.db_name)
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        print(f"Connected to database at: {db_path}")
    
    def load_bird_data(self, excel_path: str):
        """Load bird data from Excel file with multi-level headers"""
        try:
            # Read Excel with both header rows
            print(f"Reading Excel file: {excel_path}")
            df = pd.read_excel(excel_path, header=[0, 1])
            
            # Show original headers
            print("\nOriginal headers:")
            print(df.columns.values)
            
            # Combine the two levels into single column names
            new_columns = []
            for col in df.columns:
                # Clean and combine the two levels
                top_level = str(col[0]).strip().lower()
                second_level = str(col[1]).strip().lower()
                
                # Handle cases where top level is empty/NaN
                if pd.isna(top_level) or top_level == 'nan' or top_level == '':
                    new_col = second_level
                else:
                    new_col = f"{top_level}_{second_level}"
                
                # Clean the combined name
                new_col = new_col.replace(' ', '_').replace('(', '').replace(')', '')
                new_columns.append(new_col)
            
            # Assign new column names
            df.columns = new_columns
            
            print("\nNew combined column names:")
            for col in new_columns:
                print(col)
            
            print(f"\nSuccessfully loaded data with {len(df)} records")
            return df
            
        except Exception as e:
            print(f"Error reading Excel file: {str(e)}")
            return None
    
    def create_birds_table(self, df: pd.DataFrame):
        """Create table based on bird data structure"""
        # Drop existing table if it exists
        self.cursor.execute("DROP TABLE IF EXISTS birds")
        
        # Get column types
        dtype_mapping = {
            'object': 'TEXT',
            'int64': 'INTEGER',
            'float64': 'FLOAT',
            'datetime64[ns]': 'TIMESTAMP',
            'bool': 'BOOLEAN'
        }
        
        # Create columns string for SQL
        columns = []
        for col, dtype in df.dtypes.items():
            sql_type = dtype_mapping.get(str(dtype), 'TEXT')
            columns.append(f'"{col}" {sql_type}')
        
        # Create table
        create_table_sql = f"""
        CREATE TABLE IF NOT EXISTS birds (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            {', '.join(columns)}
        )
        """
        self.cursor.execute(create_table_sql)
        print("\nCreated birds table with schema:")
        # Show table schema
        self.cursor.execute("PRAGMA table_info(birds)")
        for col in self.cursor.fetchall():
            print(f"Column: {col[1]}, Type: {col[2]}")
    
    def insert_data(self, df: pd.DataFrame):
        """Insert bird data from DataFrame into SQLite table"""
        # Replace NaN values with None for SQL
        df = df.where(pd.notnull(df), None)
        
        # Convert DataFrame to list of tuples
        values = df.to_dict('records')
        
        # Get column names
        columns = list(df.columns)
        
        # Create the INSERT statement
        placeholders = ','.join(['?' for _ in columns])
        insert_sql = f"""
        INSERT INTO birds ({','.join(columns)})
        VALUES ({placeholders})
        """
        
        # Insert the data
        for record in values:
            self.cursor.execute(insert_sql, list(record.values()))
        
        self.conn.commit()
        print(f"\nInserted {len(df)} records into birds table")
        
        # Show sample data
        print("\nFirst few records in database:")
        self.cursor.execute("SELECT * FROM birds LIMIT 2")
        records = self.cursor.fetchall()
        for record in records:
            print(record)
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
            print("\nDatabase connection closed")

def setup_bird_knowledge():
    """Main setup function"""
    setup = BirdKnowledgeSetup()
    setup.connect_db()
    
    try:
        # Load data - make sure excel file is in the same directory
        df = setup.load_bird_data("bird_data.xlsx")  # Just pass the filename
        
        if df is not None:
            setup.create_birds_table(df)
            setup.insert_data(df)
            
    finally:
        setup.close()

if __name__ == "__main__":
    setup_bird_knowledge()