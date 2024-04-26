from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import plotly.express as px

app = Flask(__name__)

# Home route
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle file upload and visualization
@app.route('/upload', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            # Read the uploaded file into a pandas DataFrame
            df = pd.read_csv(file, encoding='latin-1')

            # Get form inputs for customization
            x_column = request.form.get('x_column')
            y_column = request.form.get('y_column')
            color_column = request.form.get('color_column')
            title = request.form.get('title')
            chart_type = request.form.get('chart_type')

            # Create a plotly figure
            if chart_type == 'scatter':
                fig = px.scatter(df, x=x_column, y=y_column, color=color_column, title=title)
            elif chart_type == 'line':
                fig = px.line(df, x=x_column, y=y_column, color=color_column, title=title)
            elif chart_type == 'area':
                fig = px.area(df, x=x_column, y=y_column, color=color_column, title=title)
            elif chart_type == 'bar':
                fig = px.bar(df, x=x_column, y=y_column, color=color_column, title=title)
            elif chart_type == 'histogram':
                fig = px.histogram(df, x=x_column, color=color_column, title=title)
            elif chart_type == 'box':
                fig = px.box(df, x=x_column, y=y_column, color=color_column, title=title)
            elif chart_type == 'pie':
                fig = px.pie(df, values=y_column, names=x_column, title=title)
            elif chart_type == 'scatter_matrix':
                fig = px.scatter_matrix(df, dimensions=[x_column, y_column], color=color_column, title=title)

                # Not directly supported by Plotly Express, you may need to use other libraries like matplotlib
                return "Venn diagram is not directly supported by Plotly Express"
            else:
                return "Unsupported chart type"

            # Convert the Plotly figure to HTML
            plot_html = fig.to_html(full_html=False)

            return render_template('visualization.html', plot_html=plot_html)

    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)
