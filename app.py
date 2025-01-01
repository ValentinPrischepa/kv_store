
import logging

from flask import Flask, request, jsonify
from kv_store.kv_service import KeyValueService

app = Flask(__name__)
app.logger.setLevel(logging.INFO)
kv_store = KeyValueService()
kv_store.init_hash_map()


@app.route('/key-value', methods=['POST'])
def add_entry():
    data = request.json
    key = data.get('key')
    value = data.get('value')
    if not key or value is None:
        return jsonify({"Error": "Both key and value are required"}), 400
    kv_store.put_entry(key, value)
    return jsonify({"message": f"key '{key}' added successfully"}), 201


@app.route('/key-value/<key>', methods=['GET'])
def get_entry(key):
    value = kv_store.find_entry(key)
    if value is None:
        return jsonify({"error": f"Key '{key}' not found or was deleted"}), 404
    return jsonify({"key": key, "value": value}), 200


@app.route('/key-value/<key>', methods=['DELETE'])
def delete_entry(key):
    kv_store.delete_entry(key)
    return jsonify({"message": f"key {key} was deleted"}), 200


@app.route('/key-value/all-keys', methods=['GET'])
def get_all_keys():
    return jsonify(kv_store.get_all_keys()), 200


@app.route('/key-value/compaction', methods=['POST'])
def run_file_compaction():
    file_name = kv_store.compact_log_file()
    return jsonify({"message": f"File {file_name} has been compacted"}), 200


@app.route('/key-value/purge_kv', methods=['POST'])
def purge_kv():
    file_name = kv_store.purge_kv()
    return jsonify({"message": f"KV Storage was purged for file {file_name}"}), 200


if __name__ == '__main__':
    app.run(debug=True)
