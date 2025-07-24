def generate_report(timeline_df, graph):
    """
    Generates a text report from a timeline and a connection graph.

    Args:
        timeline_df (pd.DataFrame): A DataFrame with timeline information.
        graph (networkx.Graph): A connection graph.

    Returns:
        str: A string containing the report.
    """
    report = "--- Timeline ---\n"
    for index, row in timeline_df.iterrows():
        report += f"[{row['timestamp'].strftime('%Y-%m-%d')}] {row['text']}\n"

    report += "\n--- Connections ---\n"
    for node in graph.nodes():
        connections = list(graph.neighbors(node))
        if connections:
            report += f"{node} is connected to: {', '.join(connections)}\n"

    return report
