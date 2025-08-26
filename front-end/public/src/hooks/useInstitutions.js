import { useState, useEffect, useCallback } from 'react';
import { getInstitutionsByUf, createInstitution, updateInstitution, deleteInstitution } from '../services/api.js';

export function useInstitutions(selectedState) {
  const [institutions, setInstitutions] = useState([]);
  const [loading, setLoading] = useState(false);

  const fetchInstitutions = useCallback(async () => {
    if (!selectedState) {
      setInstitutions([]);
      return;
    }
    setLoading(true);
    try {
      const data = await getInstitutionsByUf(selectedState.sigla);
      setInstitutions(data);
    } catch (error) {
      console.error("Erro ao buscar instituições:", error);
      alert(`Erro ao buscar dados: ${error.message}`);
    } finally {
      setLoading(false);
    }
  }, [selectedState]);

  useEffect(() => {
    fetchInstitutions();
  }, [fetchInstitutions]);

  const addInstitution = async (formData) => {
    const newInstitution = await createInstitution(formData);
    setInstitutions(prev => [...prev, newInstitution]);
  };

  const editInstitution = async (id, ano, formData) => {
    const updatedInstitution = await updateInstitution(id, ano, formData);
    setInstitutions(prev => prev.map(inst => 
      (inst.id === id && inst.ano === ano) ? updatedInstitution : inst
    ));
  };

  const removeInstitution = async (id, ano) => {
    await deleteInstitution(id, ano);
    setInstitutions(prev => prev.filter(inst => 
        !(String(inst.id) === String(id) && String(inst.ano) === String(ano))
    ));
  };

  return {
    institutions,
    loading,
    addInstitution,
    editInstitution,
    removeInstitution,
  };
}