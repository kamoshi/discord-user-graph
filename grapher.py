import matplotlib.pyplot as plt
import networkx as nx
import json


def convert_to_percentages(main_tree):
    author_sums = {}  # sum of messages sent near a person
    # for each person sum total messages sent by others in vicinity
    for author, sub_tree in main_tree.items():
        sum_all = 0
        for _, value in sub_tree.items():
            sum_all += value
        author_sums[author] = sum_all

    percents = {}       # result dictionary
    # already_added = set()  # set of connections already added

    for a, sub_tree in main_tree.items():  # a stands for author of a message
        percents[a] = {}
        for n, _ in sub_tree.items():  # n stands for neighbors
            # if (author, neighbor) in already_added or (neighbor, author) in already_added:
            #    continue  # this connection already added
            top = (main_tree[a][n] + main_tree[n][a])
            bottom = (author_sums[a] + author_sums[n])
            edge_calc = (top/bottom) ** .5
            percents[a][n] = edge_calc
            # already_added.add((author, neighbor))

    return percents


# LOAD DATA
with open('result.json') as json_input:
    data = json.load(json_input)
    message_data = data["message_data"]
    username_data = data["username_data"]
    percent_data = convert_to_percentages(message_data)


def retrieve_name(user_id):
    if user_id in username_data:
        name = username_data[user_id]
        return name  # .join(e for e in name if e.isalnum())
    else:
        return user_id


def draw_main_graph():

    G = nx.Graph()

    for author, sub_tree in percent_data.items():
        author_name = retrieve_name(author)

        for neighbor, percent in sub_tree.items():
            G.add_edge(author_name, retrieve_name(neighbor), weight=percent / 10)

    pos = nx.spring_layout(G)

    all_edges = [(u, v) for (u, v, d) in G.edges(data=True)]
    all_widths = [(d['weight'] * 30) for (_, _, d) in G.edges(data=True)]

    nx.draw_networkx_edges(G, pos, edgelist=all_edges, width=all_widths, alpha=1)

    # NODES
    nx.draw_networkx_nodes(G, pos, node_size=100, alpha=0.5)

    # LABELS
    nx.draw_networkx_labels(G, pos, font_size=10, font_family='sans-serif')

    fig = plt.gcf()
    fig.canvas.set_window_title("Kirby's Weed Shop")
    fig.tight_layout()
    plt.axis('off')
    fig_manager = plt.get_current_fig_manager()
    fig_manager.window.showMaximized()
    plt.show()


def draw_personal_graphs():

    for author, sub_tree in percent_data.items():
        author_name = retrieve_name(author)

        G = nx.Graph()

        for neighbor, percent in sub_tree.items():
            G.add_edge(author_name, retrieve_name(neighbor), weight=percent/10)

        pos = nx.spring_layout(G)

        all_edges = [(u, v) for (u, v, d) in G.edges(data=True)]
        all_widths = [(d['weight'] * 30) for (_, _, d) in G.edges(data=True)]

        # NODES
        nx.draw_networkx_nodes(G, pos, node_size=100, alpha=0.5)

        # EDGES
        nx.draw_networkx_edges(G, pos, edgelist=all_edges, width=all_widths, alpha=1)

        # LABELS
        nx.draw_networkx_labels(G, pos, font_size=10, font_family='sans-serif')

        fig = plt.gcf()
        fig.canvas.set_window_title(author_name)
        fig.tight_layout()
        plt.axis('off')
        fig_manager = plt.get_current_fig_manager()
        fig_manager.window.showMaximized()
        plt.show()


def main():
    draw_main_graph()
    draw_personal_graphs()


if __name__ == '__main__':
    main()

