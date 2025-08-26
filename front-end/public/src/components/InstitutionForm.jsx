import React, { useState, useEffect } from 'react';

const InstitutionForm = ({ title, onSave, onCancel, initialData = {}, isEditing = false }) => {
  const [formData, setFormData] = useState({
    CO_ENTIDADE: '',
    NO_ENTIDADE: '',
    NO_MUNICIPIO: '',
    CO_UF: '',
    NO_UF: '',
    SG_UF: '',
    QT_MAT_INF: 0,
    QT_MAT_FUND: 0,
    ano: ''
  });

  useEffect(() => {

    const mappedData = {
        CO_ENTIDADE: initialData.id || initialData.CO_ENTIDADE || '',
        NO_ENTIDADE: initialData.nome || initialData.NO_ENTIDADE || '',
        NO_MUNICIPIO: initialData.municipio || initialData.NO_MUNICIPIO || '',
        CO_UF: initialData.uf_codigo || initialData.CO_UF || '',
        NO_UF: initialData.uf_nome || initialData.NO_UF || '',
        SG_UF: initialData.uf_sigla || initialData.SG_UF || '',
        QT_MAT_INF: initialData.qt_mat_inf || initialData.QT_MAT_INF || 0,
        QT_MAT_FUND: initialData.qt_mat_fund || initialData.QT_MAT_FUND || 0,
        ano: initialData.ano || ''
    };
    setFormData(mappedData);
  }, [initialData]);

  const handleChange = (e) => {
    const { name, value, type } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: type === 'number' ? parseInt(value, 10) || 0 : value
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onSave(formData);
  };

  return (
    <div className="modal">
      <div className="modal-content">
        <h2>{title}</h2>
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label>Código da Entidade</label>
            <input type="number" name="CO_ENTIDADE" value={formData.CO_ENTIDADE} onChange={handleChange} required disabled={isEditing} />
          </div>
          <div className="form-group">
            <label>Ano do Censo</label>
            <input type="number" name="ano" value={formData.ano} onChange={handleChange} required disabled={isEditing} />
          </div>
          <div className="form-group">
            <label>Nome da Entidade</label>
            <input type="text" name="NO_ENTIDADE" value={formData.NO_ENTIDADE} onChange={handleChange} required />
          </div>
          <div className="form-group">
            <label>Município</label>
            <input type="text" name="NO_MUNICIPIO" value={formData.NO_MUNICIPIO} onChange={handleChange} required />
          </div>
          <div className="form-group">
            <label>Código da UF</label>
            <input type="number" name="CO_UF" value={formData.CO_UF} onChange={handleChange} required />
          </div>
          <div className="form-group">
            <label>Nome da UF</label>
            <input type="text" name="NO_UF" value={formData.NO_UF} onChange={handleChange} required />
          </div>
          <div className="form-group">
            <label>Sigla da UF</label>
            <input type="text" name="SG_UF" value={formData.SG_UF} onChange={handleChange} required maxLength="2" />
          </div>
          <div className="form-group">
            <label>Matrículas (Infantil)</label>
            <input type="number" name="QT_MAT_INF" value={formData.QT_MAT_INF} onChange={handleChange} />
          </div>
          <div className="form-group">
            <label>Matrículas (Fundamental)</label>
            <input type="number" name="QT_MAT_FUND" value={formData.QT_MAT_FUND} onChange={handleChange} />
          </div>
          <div className="form-actions">
            <button type="submit" className="save-btn">Salvar</button>
            <button type="button" onClick={onCancel}>Cancelar</button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default InstitutionForm;

