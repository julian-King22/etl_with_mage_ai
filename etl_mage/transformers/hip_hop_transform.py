if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def transform(data, *args, **kwargs):
    """
    Template code for a transformer block.

    Add more parameters to this function if this block has multiple parent blocks.
    There should be one parameter for each output variable from each parent block.

    Args:
        data: The output from the upstream parent block
        args: The output from any additional upstream blocks (if applicable)

    Returns:
        Anything (e.g. data frame, dictionary, array, int, str, etc.)
    """
    # Specify your transformation logic here
    import pandas as pd

    hip_hop_artists_death_df = pd.DataFrame(data)
    hip_hop_artists_death_df.columns = hip_hop_artists_death_df.columns.str.lower().str.replace(' ', '_')

    selected_columns = list(hip_hop_artists_death_df.columns)
    selected_columns.remove('ref.')
    selected_columns.remove("unnamed:_0")

    # list(hip_hop_artists_death_df.columns))
    from datetime import datetime
    hip_hop_artists_death_df = hip_hop_artists_death_df[selected_columns]

    date_strings = hip_hop_artists_death_df['date_of_death'].astype(str)
    
    date_objects = pd.to_datetime(hip_hop_artists_death_df['date_of_death'], format="%B %d, %Y")

    # Extract the month names
    month_of_death = date_objects.dt.strftime("%B")
    year_of_death = date_objects.dt.strftime("%Y")

    hip_hop_artists_death_df['month_of_death'] = month_of_death
    hip_hop_artists_death_df['year_of_death'] = year_of_death

    
    hip_hop_artists_death_df['state'] = hip_hop_artists_death_df['place_of_death'].str.split(',').str[-2]
    hip_hop_artists_death_df['country'] = hip_hop_artists_death_df['place_of_death'].str.split(',').str[-1]
    hip_hop_artists_death_df['country'] = hip_hop_artists_death_df['country'].str.strip().replace({'U.S.': 'USA'})
    
    hip_hop_artists_death_df.columns = hip_hop_artists_death_df.columns.str.replace('state',"state_of_death")
    hip_hop_artists_death_df.columns = hip_hop_artists_death_df.columns.str.replace('country',"country_of_death")

    # return True
    return hip_hop_artists_death_df


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
