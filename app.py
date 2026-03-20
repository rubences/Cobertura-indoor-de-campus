from flask import Flask, render_template, request, jsonify, send_file
import io
from utils import calculate_coverage, get_default_points, get_default_bands, DATA_THRESHOLD_DBM, VOICE_THRESHOLD_DBM

app = Flask(__name__)

@app.route('/')
def index():
    """Página principal."""
    points = get_default_points()
    bands = get_default_bands()
    return render_template('index.html', points=points, bands=bands, 
                         data_threshold=DATA_THRESHOLD_DBM, 
                         voice_threshold=VOICE_THRESHOLD_DBM)

@app.route('/api/calculate', methods=['POST'])
def calculate():
    """Endpoint para calcular cobertura."""
    try:
        data = request.json
        
        # Extraer puntos del formulario
        points = []
        num_points = int(data.get('num_points', 3))
        for i in range(num_points):
            point = {
                'nombre': data.get(f'punto_{i}_nombre', f'Punto {i+1}'),
                'planta': data.get(f'punto_{i}_planta', 'Baja'),
                'altura_m': float(data.get(f'punto_{i}_altura', 1.5)),
                'dist_h_m': float(data.get(f'punto_{i}_dist', 180)),
                'fachada_db': float(data.get(f'punto_{i}_fachada', 14)),
                'paredes_db': float(data.get(f'punto_{i}_paredes', 0)),
                'forjados_db': float(data.get(f'punto_{i}_forjados', 0)),
                'extra_db': float(data.get(f'punto_{i}_extra', 0)),
            }
            points.append(point)
        
        # Extraer bandas seleccionadas
        bands = {}
        available_bands = get_default_bands()
        for band_name in available_bands:
            if data.get(f'banda_{band_name}', False):
                bands[band_name] = available_bands[band_name]
        
        if not bands:
            bands = {'LTE 1800': 1800}
        
        # Calcular
        results_df = calculate_coverage(points, bands)
        
        # Preparar respuesta
        results = {
            'main': results_df[results_df['banda'] == 'LTE 1800'][['punto', 'planta', 'L_ext_db', 'L_fachada_db', 'L_paredes_db', 'L_forjados_db', 'L_extra_db', 'L_total_db', 'P_rx_dbm', 'estado', 'recomendacion']].to_dict('records') if 'LTE 1800' in bands else [],
            'comparison': results_df.pivot(index='punto', columns='banda', values='P_rx_dbm').round(1).to_dict() if len(bands) > 1 else {},
            'summary': results_df[results_df['banda'].isin(list(bands.keys()))][['punto', 'banda', 'P_rx_dbm', 'estado', 'recomendacion']].to_dict('records'),
        }
        
        return jsonify(results)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/export-csv', methods=['POST'])
def export_csv():
    """Exportar resultados a CSV."""
    try:
        data = request.json
        
        # Procesar datos igual que en calculate()
        points = []
        num_points = int(data.get('num_points', 3))
        for i in range(num_points):
            point = {
                'nombre': data.get(f'punto_{i}_nombre', f'Punto {i+1}'),
                'planta': data.get(f'punto_{i}_planta', 'Baja'),
                'altura_m': float(data.get(f'punto_{i}_altura', 1.5)),
                'dist_h_m': float(data.get(f'punto_{i}_dist', 180)),
                'fachada_db': float(data.get(f'punto_{i}_fachada', 14)),
                'paredes_db': float(data.get(f'punto_{i}_paredes', 0)),
                'forjados_db': float(data.get(f'punto_{i}_forjados', 0)),
                'extra_db': float(data.get(f'punto_{i}_extra', 0)),
            }
            points.append(point)
        
        bands = {}
        available_bands = get_default_bands()
        for band_name in available_bands:
            if data.get(f'banda_{band_name}', False):
                bands[band_name] = available_bands[band_name]
        
        if not bands:
            bands = {'LTE 1800': 1800}
        
        results_df = calculate_coverage(points, bands)
        
        # Exportar a CSV
        output = io.StringIO()
        results_df.to_csv(output, index=False)
        output.seek(0)
        
        return send_file(
            io.BytesIO(output.getvalue().encode()),
            mimetype='text/csv',
            as_attachment=True,
            download_name='resultados_cobertura.csv'
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
