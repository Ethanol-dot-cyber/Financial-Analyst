from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

def get_explanation(metric, value):
    """Return a pre-written explanation based on metric value."""
    try:
        value = float(value)
    except:
        return "Invalid value."

    if metric == "ROI":
        if value < 0:
            return "ROI is negative, meaning costs exceed gains. The company may be losing money and should review expenses."
        elif value < 50:
            return "ROI is moderate. Gains slightly exceed costs, indicating average efficiency."
        else:
            return "ROI is high, gains greatly exceed costs. This shows strong profitability and efficient investment."

    elif metric == "Break-even Units":
        if value > 1000:
            return "Break-even units are high, meaning you need to sell a lot to cover costs. Consider reducing expenses or increasing margins."
        elif value > 100:
            return "Break-even units are moderate, manageable for your business."
        else:
            return "Break-even units are low, meaning the company covers costs quickly and can be profitable with fewer sales."

    elif metric == "Net Profit Margin":
        if value < 10:
            return "Net Profit Margin is low; only a small portion of revenue becomes profit. Cost management or pricing strategies may help."
        elif value < 30:
            return "Net Profit Margin is moderate; the company earns reasonable profit from revenue."
        else:
            return "Net Profit Margin is high; the company keeps a large portion of revenue as profit, indicating strong efficiency."

    elif metric == "ROA":
        if value < 5:
            return "ROA is low; the company is not effectively using assets to generate profits."
        elif value < 15:
            return "ROA is moderate; assets are generating a fair amount of return."
        else:
            return "ROA is high; assets are being used very efficiently to generate profits."

    elif metric == "ROE":
        if value < 5:
            return "ROE is low; shareholders are receiving poor returns on their equity."
        elif value < 15:
            return "ROE is moderate; shareholders get a fair return."
        else:
            return "ROE is high; shareholders benefit from strong profitability."

    elif metric == "EPS":
        if value < 1:
            return "EPS is low; each share earns little, indicating low profitability per share."
        elif value < 5:
            return "EPS is moderate; shareholders earn a reasonable amount per share."
        else:
            return "EPS is high; each share generates strong earnings, indicating healthy financial performance."

    else:
        return "No explanation available."

@app.route("/")
def index():
    return render_template("financialanalyst.html")

@app.route("/calculate", methods=["POST"])
def calculate():
    data = request.get_json()  # <-- make sure to use get_json()
    metric = data.get("metric")

    try:
        if metric == "ROI":
            revenue = float(data.get("revenue", 0))
            costs = float(data.get("costs", 0))
            value = 0 if costs == 0 else round((revenue - costs)/costs * 100, 2)

        elif metric == "Break-even Units":
            fixed = float(data.get("fixed", 0))
            revenue_per_unit = float(data.get("revenue_per_unit", 0))
            cogs = float(data.get("cogs", 0))
            value = 0 if revenue_per_unit - cogs == 0 else round(fixed / (revenue_per_unit - cogs), 2)

        elif metric == "Net Profit Margin":
            revenue = float(data.get("revenue", 0))
            costs = float(data.get("costs", 0))
            value = 0 if revenue == 0 else round((revenue - costs)/revenue * 100, 2)

        elif metric == "ROA":
            revenue = float(data.get("revenue", 0))
            costs = float(data.get("costs", 0))
            assets = float(data.get("assets", 0))
            value = 0 if assets == 0 else round((revenue - costs)/assets * 100, 2)

        elif metric == "ROE":
            revenue = float(data.get("revenue", 0))
            costs = float(data.get("costs", 0))
            equity = float(data.get("equity", 0))
            value = 0 if equity == 0 else round((revenue - costs)/equity * 100, 2)

        elif metric == "EPS":
            revenue = float(data.get("revenue", 0))
            costs = float(data.get("costs", 0))
            shares = float(data.get("shares", 1))
            value = 0 if shares == 0 else round((revenue - costs)/shares, 2)

        else:
            value = 0

    except:
        value = 0

    explanation = get_explanation(metric, value)
    return jsonify({"value": value, "explanation": explanation})

if __name__ == "__main__":
    app.run(debug=True)
