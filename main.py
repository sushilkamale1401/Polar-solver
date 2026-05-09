from flask import Flask, render_template_string, request
import sympy as sp

app = Flask(__name__)

# This is the HTML layout for your website
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Polar Integral Solver</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f4f7f6; display: flex; justify-content: center; padding: 40px; }
        .card { background: white; padding: 30px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); width: 100%; max-width: 500px; }
        h2 { color: #2c3e50; text-align: center; }
        input { width: 100%; padding: 10px; margin: 10px 0; border: 1px solid #ddd; border-radius: 5px; box-sizing: border-box; }
        button { width: 100%; padding: 12px; background-color: #3498db; color: white; border: none; border-radius: 5px; cursor: pointer; font-size: 16px; }
        button:hover { background-color: #2980b9; }
        .result-box { margin-top: 25px; padding: 15px; background-color: #e8f4fd; border-radius: 8px; border-left: 5px solid #3498db; word-wrap: break-word; }
    </style>
</head>
<body>
    <div class="card">
        <h2>Polar Transformation</h2>
        <form method="POST">
            <label>Cartesian Function f(x, y):</label>
            <input type="text" name="expr" placeholder="e.g. x**2 + y**2" required>
            
            <label>r limits (start, end):</label>
            <div style="display:flex; gap:10px;">
                <input type="text" name="r_s" placeholder="0" required>
                <input type="text" name="r_e" placeholder="1" required>
            </div>

            <label>Theta limits (start, end):</label>
            <div style="display:flex; gap:10px;">
                <input type="text" name="t_s" placeholder="0" required>
                <input type="text" name="t_e" placeholder="pi/2" required>
            </div>
            
            <button type="submit">Calculate Transformation</button>
        </form>

        {% if result %}
        <div class="result-box">
            <strong>Transformed Polar (f * r):</strong><br> {{ polar_expr }} <br><br>
            <strong>Final Integral Result:</strong><br> {{ result }}
        </div>
        {% endif %}
    </div>
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def home():
    result = None
    polar_expr = None
    if request.method == 'POST':
        try:
            x, y, r, theta = sp.symbols('x y r theta')
            # Get user input
            f_xy = sp.sympify(request.form['expr'])
            
            # Transformation Logic (From your provided code)
            f_polar = f_xy.subs({x: r*sp.cos(theta), y: r*sp.sin(theta)}) * r
            polar_expr = sp.simplify(f_polar)
            
            # Limits
            r_lim = (r, sp.sympify(request.form['r_s']), sp.sympify(request.form['r_e']))
            t_lim = (theta, sp.sympify(request.form['t_s']), sp.sympify(request.form['t_e']))
            
            # Integrate
            calc = sp.integrate(polar_expr, r_lim, t_lim)
            result = sp.pretty(calc)
        except Exception as e:
            result = f"Error: {e}"
            
    return render_template_string(HTML_TEMPLATE, result=result, polar_expr=polar_expr)

if __name__ == '__main__':
    app.run(debug=True)
