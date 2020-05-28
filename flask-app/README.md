# Flask for IHC Database

- Connects with IHC Database through a flask integration with MySQL.
- Runs at: `http://localhost:5000`

### Prerequisites
- Have `python3` installed
- Have `pip` installed
- Have `virtualenv` installed

### Installing
1. On terminal go to `/flask-app` folder
2. Create a virtual environment with `virtualenv -p python3 venv`
3. Activate virtual environment with `.venv/bin/activate`
4. Run `pip install -r requirements.txt`
2. Run `export FLASK_ENV=development`
3. Run `flask run`

Your flask app should be up and running!
Check for the return `HomePage` at `http://localhost:5000`

### Troubleshooting

If a MySQL x Flask error is thrown try reinstalling `mysqlclient`
```bash
pip uninstall mysqlclient
pip install mysqlclient
```

### Routes

#### All papers
Route: `http://localhost:5000/papers` \
Return model:
```json
{
  "1998": [
    [4506,"Uma Abordagem Semi\u00f3tica \u00e0 An\u00e1lise de Interfaces: um estudo de caso"],
    [4507,"Knowledge and Communication Perspectives in Extensible Applications"]
  ],
  "2008":[
    [4636,"A Express\u00e3o da Diversidade de Usu\u00e1rios no Projeto de Intera\u00e7\u00e3o com Padr\u00f5es e Personas"]
  ]
}
```

#### Paper by ID
Route: `http://localhost:5000/papers/<int:id>` \
Return model:
```json
{
  "abstract_PT": "NA", 
  "authors": [
    "Lucia Vilela Leite Filgueiras", 
    "Pl\u00ednio Thomaz Aquino Junior"
  ], 
  "title": "A Express\u00e3o da Diversidade de Usu\u00e1rios no Projeto de Intera\u00e7\u00e3o com Padr\u00f5es e Personas"
}
```

#### Paper references
Route: `http://localhost:5000/papers/<int:id>/references` \
Return model:
```json
{
  "cited": ["4222", "4060"], 
  "citedBy": ["4380"]
}
```

## Authors
- Gabriela Gutierrez - @gabibguti