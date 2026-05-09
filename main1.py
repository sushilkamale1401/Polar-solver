from flask import Flask, render_template_string, request
import sympy as sp
import time

app = Flask(__name__)

# Enhanced HTML with Simulation/MathJax
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Polar Integral Solver</title>
    <script src="https://polyfill.io/v3/polyfill.min.js?features=es6"></script>
    <script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
    <style>
        body { font-family: 'Segoe UI', sans-serif; background-color: #f0f2f5; display: flex; justify-content: center; padding: 40px; }
        .card { background: white; padding: 30px; border-radius: 12px; box-shadow: 0 10px 25px rgba(0,0,0,0.1); width: 100%; max-width: 600px; }
        h2 { color: #1a73e8; text-align: center; margin-bottom: 25px; }
        label { font-weight: 600; font-size: 14px; color: #5f6368; }
        input { width: 100%; padding: 12px; margin: 8px 0 20px 0; border: 1px solid #dadce0; border-radius: 6px; box-sizing: border-box; transition: 0.3s; }
        input:focus { border-color: #1a73e8; outline: none; box-shadow: 0 0 0 2px rgba(26,115,232,0.2); }
        button { width: 100%; padding: 14px; background-color: #1a73e8; color: white; border: none; border-radius: 6px; cursor: pointer; font-size: 16px; font-weight: bold; }
        button:hover { background-color: #1557b0; }
        
        /* Simulation Styles */
        #simulation-overlay { display: none; margin-top: 20px; text-align: center; }
        .spinner { border: 4px solid #f3f3f3; border-top: 4px solid #3498db; border-radius: 50%; width: 30px; height: 30px; animation: spin 1s linear infinite; margin: 10px auto; }
        @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
        
        .result-box { margin-top: 25px; padding: 20px; background-color: #ffffff; border: 1px solid #e0e0e0; border-radius: 8px; border-left: 6px solid #1a73e8; }
        .math-display { font-size: 1.2em; overflow-x: auto; padding: 10px 0; }
    </style>
</head>
<body>
    <div class="card">
        <h2>Polar Engine v2.1</h2>
        <form id="calcForm" method="POST" onsubmit="showSimulation()">
            <label>Cartesian Function \( f(x, y) \):</label>
            <input type="text" name="expr" placeholder="e.g. x**2 + y**2" required>
            
            <div style="display:flex; gap:15px;">
                <div style="flex:1;">
                    <label>\( r \) limits (start, end):</label>
                    <input type="text" name="r_s" placeholder="0" required>
                    <input type="text" name="r_e" placeholder="1" required>
                </div>
                <div style="flex:1;">
                    <label>\( \theta \) limits (start, end):</label>
                    <input type="text" name="t_s" placeholder="0" required>
                    <input type="text" name="t_e" placeholder="pi" required>
                </div>
            </div>
            
            <button type="submit">Execute Transformation</button>
        </form>

        <div id="simulation-overlay">
            <div class="spinner"></div>
            <p id="sim-text" style="color: #666; font-style: italic;">Initializing Jacobian transformation...</p>
        </div>

        {% if result %}
        <div id="result-container" class="result-box">
            <p><strong>Step 1: Polar Mapping \( f(r, \theta) \cdot r \)</strong></p>
            <div class="math-display">
                $${{ polar_latex }}$$
            </div>
            <hr style="border: 0; border-top: 1px solid #eee;">
            <p><strong>Step 2: Computed Integral</strong></p>
            <div class="math-display">
                $${{ result_latex }}$$
            </div>
        </div>
        {% endif %}
    </div>

    <script>
        function showSimulation() {
            document.getElementById('simulation-overlay').style.display = 'block';
            if(document.getElementById('result-container')) {
                document.getElementById('result-container').style.opacity = '0.3';
            }
            
            const steps = [
                "Applying \( x = r \cos(\theta) \)...",
                "Applying \( y = r \sin(\theta) \)...",
                "Multiplying by Jacobian determinant \( r \)...",
                "Evaluating double integral..."
            ];
            let i = 0;
            const textEl = document.getElementById('sim-text');
            setInterval(() => {
                if(i < steps.length) {
                    textEl.innerHTML = steps[i];
                    i++;
                }
            }, 600);
        }
    </script>
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def home():
    result_latex = None
    polar_latex = None
    if request.method == 'POST':
        try:
            x, y, r, theta = sp.symbols('x y r theta')
            
            # Parsing and Transformation
            f_xy = sp.sympify(request.form['expr'])
            f_polar = f_xy.subs({x: r*sp.cos(theta), y: r*sp.sin(theta)}) * r
            polar_expr = sp.simplify(f_polar)
            polar_latex = sp.latex(polar_expr)
            
            # Define limits
            r_lim = (r, sp.sympify(request.form['r_s']), sp.sympify(request.form['r_e']))
            t_lim = (theta, sp.sympify(request.form['t_s']), sp.sympify(request.form['t_e']))
            
            # Perform Integration
            calc = sp.integrate(polar_expr, r_lim, t_lim)
            result_latex = sp.latex(calc)
            
        except Exception as e:
            result_latex = f"\\text{{Error: {str(e)}}}"
            
    return render_template_string(HTML_TEMPLATE, result=result_latex, 
                                 result_latex=result_latex, polar_latex=polar_latex)

if __name__ == '__main__':
    app.run(debug=True)
