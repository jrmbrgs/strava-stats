stats = """
select
    weekno,
    current_weekno,
    cumulative_nb_run_2023,
    cumulative_nb_run_2024,
    cumulative_distance_2023,
    cumulative_distance_2024,
    cumulative_elapsed_time_2023,
    cumulative_elapsed_time_2024,
    cumulative_elevation_gain_2023,
    cumulative_elevation_gain_2024,
  from strava.activities_stats
  order by weekno
"""
