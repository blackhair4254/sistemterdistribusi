from flask import Flask, jsonify, request, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Konfigurasi koneksi MySQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/inventory'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Model database
class Stock(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sku = db.Column(db.String(100), nullable=False)
    nama_barang = db.Column(db.String(100), nullable=False)
    jumlah_stok = db.Column(db.Integer, nullable=False)

# Endpoint untuk mendapatkan semua stok barang
@app.route('/api/get_stocks', methods=['GET'])
def get_stocks():
    stocks = Stock.query.all()
    result = [{"sku": s.sku, "nama_barang": s.nama_barang, "jumlah_stok": s.jumlah_stok} for s in stocks]
    return jsonify(result)

@app.route('/api/get_stocks/<string:sku>', methods=['GET'])
def get_stocks_one(sku):
    # Query untuk mendapatkan stok barang berdasarkan ID
    stock = Stock.query.filter_by(sku=sku).first()

    # Jika stok tidak ditemukan, kembalikan respons error
    if stock is None:
        return jsonify({"message": "Stock not found"}), 404

    # Jika ditemukan, kembalikan data stok dalam format JSON
    result = {
        "sku": stock.sku,
        "nama_barang": stock.nama_barang,
        "jumlah_stok": stock.jumlah_stok
    }
    return jsonify(result)


# Endpoint untuk mengupdate stok barang
@app.route('/api/stocks/<int:id>', methods=['PUT'])
def update_stock(id):
    data = request.json
    stock = Stock.query.get_or_404(id)
    stock.jumlah_stok = data.get('jumlah_stok', stock.jumlah_stok)
    db.session.commit()
    return jsonify({"message": "Stock updated successfully", "id": stock.id})

# UI sederhana untuk menampilkan stok barang
@app.route('/')
def index():
    stocks = Stock.query.all()
    return render_template('stock.html', stocks=stocks)

# Inisialisasi database
def initialize_database():
    with app.app_context():
        db.create_all()
        if Stock.query.count() == 0:
            db.session.add(Stock(nama_barang="celana jeans",sku="SKU01", jumlah_stok=10))
            db.session.add(Stock(nama_barang="daster dobblet",sku="SKU02", jumlah_stok=10))
            db.session.add(Stock(nama_barang="sweater",sku="SKU03", jumlah_stok=15))
            db.session.commit()

if __name__ == '__main__':
    initialize_database()  # Inisialisasi tabel sebelum menjalankan aplikasi
    app.run(debug=True)
