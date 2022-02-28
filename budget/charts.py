import plotly.graph_objects as go
from .models import Category


def get_pie_div(mon):
    cats = Category.objects.filter(month=mon).all()
    categories = [cat.name for cat in cats]
    values=[cat.sum_spendings() for cat in cats]

    fig = go.Figure()
    fig.add_trace(
        go.Pie(
            labels=categories,
            values=values,
            marker_line_color='#000000',
            marker_line_width=2,
            textfont_size=20,
        )
    )

    fig.update_layout(
    title='Structure of your spendings',
    title_font_size=24,
    )

    div = fig.to_html(full_html=False)
    return div
