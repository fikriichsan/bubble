import os, pickle, re
from bubble.strukturdata import AVL_Tree
from bubble import app
from bs4 import BeautifulSoup

KEYWORD_FILE = os.path.join(app.root_path, "static", "keyword.dll")
LOKASI_FILE = os.path.join(app.root_path, "static", "lokasi.dll")

def set_strukdat(teks, path):

	# Check keyword file
	if not os.path.exists(KEYWORD_FILE):
		avl = AVL_Tree()
	else:
		with open(KEYWORD_FILE, "rb") as kf:
			avl = pickle.load(kf)

	for key in teks:
		avl.insert(key, path)

	with open(KEYWORD_FILE, "wb") as kf:
		pickle.dump(avl, kf)

def get_data(keyword):
	# Ambil keyword dari search
	keyword = re.sub("[\W_]", " ", keyword.lower())

	# Cek apakah ada file keyword.dll
	if not os.path.exists(KEYWORD_FILE):
		return [["Tidak ada data, harap untuk mengisi data", ""]]

	# Load file keyword.dll
	with open(KEYWORD_FILE, "rb") as kf:
		avl = pickle.load(kf)

	lokasi = []
	# cari tiap keyword
	for key in keyword.split():
		dataNode = avl.query(key)
		if dataNode:
			for lok in dataNode.loc:
				if not lok in lokasi:
					lok = os.path.basename(lok)
					name = os.path.splitext(lok)
					lokasi.append([name[0], lok])

	return lokasi

def parser_teks(teks):
	x = ""
	for i in teks:
		x += f"{i.text} "
	x = re.sub("[\W_]", " ", x.lower())
	return x.split()

def set_keyword(path):
	# Parser isinya
	with open(path, "r", encoding="utf8") as f:
		soup = BeautifulSoup(f.read(), "html.parser")
		x    = soup.find_all(["p", "title", "article"])

	# Pembuatan keyword
	teks = set(parser_teks(x))

	# Memasukkan ke dalam struktur data
	set_strukdat(teks, path)

def cek_key():

	if os.path.exists(KEYWORD_FILE):
		with open(KEYWORD_FILE, "rb") as kf:
			avl = pickle.load(kf)
		return avl.get_preOrder()
	
	return ["Tidak ada file"]

def	get_file():
	pass
