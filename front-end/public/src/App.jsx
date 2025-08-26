import React, { useState, useMemo } from 'react';
import BrazilMap from './components/BrazilMap.jsx';
import InstitutionList from './components/InstitutionList.jsx';
import InstitutionForm from './components/InstitutionForm.jsx';
import { useInstitutions } from './hooks/useInstitutions.js';
import './App.css';

export default function App() {
  const [selectedState, setSelectedState] = useState(null);
  
  const { institutions, loading, addInstitution, editInstitution, removeInstitution } = useInstitutions(selectedState);

  const [yearFilter, setYearFilter] = useState('all');
  const [searchTerm, setSearchTerm] = useState('');
  const [editingInstitution, setEditingInstitution] = useState(null);
  const [isAdding, setIsAdding] = useState(false);

  const handleSave = async (formData) => {
    const isEditing = !!editingInstitution;
    try {
      if (isEditing) {
        await editInstitution(editingInstitution.id, editingInstitution.ano, formData);
        alert('Instituição atualizada com sucesso!');
      } else {
        await addInstitution(formData);
        alert('Instituição criada com sucesso!');
      }
      setEditingInstitution(null);
      setIsAdding(false);
    } catch (error) {
      console.error("Erro ao salvar instituição:", error);
      alert(`Erro ao salvar: ${error.message}`);
    }
  };

  const handleDelete = async (id, ano) => {
    if (window.confirm('Tem certeza que deseja apagar esta instituição?')) {
      try {
        await removeInstitution(id, ano);
        alert('Instituição apagada com sucesso!');
      } catch (error) {
        console.error("Erro ao apagar instituição:", error);
        alert(`Erro ao apagar: ${error.message}`);
      }
    }
  };

  const filteredInstitutions = useMemo(() => {
    return institutions
      .filter(inst => yearFilter === 'all' || inst.ano?.toString() === yearFilter)
      .filter(inst => {
        const term = searchTerm.toLowerCase();
        return inst.nome?.toLowerCase().includes(term) || inst.municipio?.toLowerCase().includes(term);
      });
  }, [institutions, yearFilter, searchTerm]);

  return (
    <div className="app-container">
      {(isAdding || editingInstitution) && <div className="modal-overlay" onClick={() => { setIsAdding(false); setEditingInstitution(null); }} />}
      
      {isAdding && (
        <InstitutionForm
          title="Adicionar Nova Instituição"
          onSave={handleSave}
          onCancel={() => setIsAdding(false)}
          initialData={{ SG_UF: selectedState?.sigla, NO_UF: selectedState?.nome }} 
        />
      )}

      {editingInstitution && (
        <InstitutionForm
          title="Editar Instituição"
          onSave={handleSave}
          onCancel={() => setEditingInstitution(null)}
          initialData={editingInstitution}
          isEditing={true}
        />
      )}

      <header>
        <h1>Mapa do Censo Escolar</h1>
        <p>Clique em um estado para ver as instituições</p>
      </header>
      <main>
        <div className="map-section">
          <BrazilMap onStateClick={setSelectedState} />
        </div>
        <div className="data-section">
          <div className="data-header">
            <h2>
              {selectedState ? `Instituições em ${selectedState.nome}` : "Nenhum estado selecionado"}
            </h2>
            {selectedState && (
              <button className="add-button" onClick={() => setIsAdding(true)}>
                Adicionar Instituição
              </button>
            )}
          </div>
          
          {selectedState && (
            <div className="filters">
              <input
                type="text"
                placeholder="Pesquisar por nome ou município..."
                className="search-bar"
                value={searchTerm}
                onChange={e => setSearchTerm(e.target.value)}
              />
              <div className="year-filter">
                <span>Filtrar por ano:</span>
                <button onClick={() => setYearFilter('all')} className={yearFilter === 'all' ? 'active' : ''}>Todos</button>
                <button onClick={() => setYearFilter('2023')} className={yearFilter === '2023' ? 'active' : ''}>2023</button>
                <button onClick={() => setYearFilter('2024')} className={yearFilter === '2024' ? 'active' : ''}>2024</button>
              </div>
            </div>
          )}

          {loading ? <p>Carregando...</p> : 
            <InstitutionList 
              institutions={filteredInstitutions}
              onEdit={setEditingInstitution}
              onDelete={handleDelete}
            />
          }
        </div>
      </main>
    </div>
  );
}