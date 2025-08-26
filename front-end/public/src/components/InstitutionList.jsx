import React from 'react';

const InstitutionList = ({ institutions, onEdit, onDelete }) => {
  if (!institutions || institutions.length === 0) {
    return <p>Nenhuma instituição encontrada para os filtros aplicados.</p>;
  }

  return (
    <ul className="institution-list">
      {institutions.map(inst => (
        <li key={`${inst.id}-${inst.ano}`}>
          <div className="inst-info">
            <strong>{inst.nome || "Nome não disponível"} (ID: {inst.id})</strong>
            <p>Local: {inst.municipio} - {inst.uf_nome} (Cód. UF: {inst.uf_codigo})</p>
            <p>Matrículas (Ano {inst.ano}): Infantil: {inst.qt_mat_inf} | Fundamental: {inst.qt_mat_fund}</p>
          </div>
          <div className="inst-actions">
            <button className="edit-btn" onClick={() => onEdit(inst)}>Editar</button>
            <button className="delete-btn" onClick={() => onDelete(inst.id, inst.ano)}>Apagar</button>
          </div>
        </li>
      ))}
    </ul>
  );
};

export default InstitutionList;
