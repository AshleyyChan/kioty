from flask import Flask, request, jsonify
from flask_cors import CORS
from knapsack import knapsack
from utils import (
    logger,
    validate_input,
    save_session_result,
    generate_session_id,
    get_history
)
from datetime import datetime
import os

# ----------------------------------
# App Setup
# ----------------------------------
app = Flask(__name__)

# Enable CORS (Restrict origin in production)
CORS(app, resources={r"/*": {"origins": "*"}})

# ----------------------------------
# Health Check Route
# ----------------------------------
@app.route("/", methods=["GET"])
def health_check():
    return "🟢 Shopping Cart Optimizer API is running."

# ----------------------------------
# Optimization Endpoint
# ----------------------------------
@app.route("/optimize", methods=["POST"])
def optimize():
    try:
        data = request.get_json()
        logger.info(f"Incoming request: {data}")

        # Validate input
        error_msg = validate_input(data)
        if error_msg:
            logger.warning(f"Validation failed: {error_msg}")
            return jsonify({"error": error_msg}), 400

        budget = data["budget"]
        items = data["items"]

        # Generate session ID
        session_id = generate_session_id()

        # Run optimization algorithm
        selected_items, total_price, total_value = knapsack(items, budget)

        result = {
            "sessionId": session_id,
            "timestamp": datetime.now().isoformat(),
            "budget": budget,
            "selectedItems": selected_items,
            "totalPrice": total_price,
            "totalValue": total_value,
            "count": len(selected_items)
        }

        logger.info(f"Session {session_id} optimized: {len(selected_items)} items, Value={total_value}, Cost={total_price}")

        # Save session result
        save_session_result(session_id, result)

        return jsonify(result)

    except Exception as e:
        logger.error(f"Unexpected error during optimization: {e}", exc_info=True)
        return jsonify({"error": "Internal server error occurred."}), 500

# ----------------------------------
# History Endpoint
# ----------------------------------
@app.route("/history", methods=["GET"])
def history():
    """
    Returns past optimization sessions (for guest user).
    Extendable to support userId in future.
    """
    try:
        history_data = get_history()
        return jsonify({"history": history_data})
    except Exception as e:
        logger.error(f"Failed to retrieve history: {e}", exc_info=True)
        return jsonify({"error": "Could not load history."}), 500

# ----------------------------------
# App Runner
# ----------------------------------
if __name__ == "__main__":
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 5050))
    logger.info(f"Starting Shopping Cart Optimizer API at http://{host}:{port}")
    app.run(host=host, port=port, debug=True)
