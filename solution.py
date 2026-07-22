import pandas as pd
import re


def add_virtual_column(df: pd.DataFrame, role: str, new_column: str) -> pd.DataFrame:
    """
    Adds a new virtual column to a pandas DataFrame based on a mathematical expression.

    Args:
        df (pd.DataFrame): The input DataFrame containing existing data.
        role (str): A mathematical expression defining the computation (e.g., 'col_a + col_b').
        new_column (str): The name of the new virtual column to be added.

    Returns:
        pd.DataFrame: A new DataFrame with the added column, or an empty DataFrame
                      if validation fails (invalid column names or rules).
    """

    # Helper function to validate labels (must consist only of letters and underscores)
    def is_valid_label(label: str) -> bool:
        return bool(re.match(r'^[a-zA-Z_]+$', str(label)))

    # 1. Validate the new_column label
    if not is_valid_label(new_column):
        return pd.DataFrame([])

    # 2. Validate all existing column labels in the provided DataFrame
    for col in df.columns:
        if not is_valid_label(col):
            return pd.DataFrame([])

    # 3. Validate the role expression characters
    # Only letters, underscores, spaces, and basic operators (+, -, *) are allowed
    if not re.match(r'^[a-zA-Z_ \+\-\*]+$', role):
        return pd.DataFrame([])

    # 4. Extract operands (column names) from the role and verify they exist in the DataFrame
    # Remove spaces and split by operators to isolate the column names
    clean_role = role.replace(" ", "")
    operands = re.split(r'[\+\-\*]', clean_role)

    for operand in operands:
        if operand not in df.columns:
            return pd.DataFrame([])

    # 5. Evaluate the expression and create the new column
    try:
        # Create a copy to prevent modifying the original input DataFrame
        result_df = df.copy()

        # Use pandas.eval for safe and efficient mathematical string evaluation
        result_df[new_column] = result_df.eval(role)

        return result_df

    except Exception:
        # Catch any unexpected evaluation errors and return an empty DataFrame
        return pd.DataFrame([])

