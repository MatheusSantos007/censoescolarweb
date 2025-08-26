const API_BASE_URL = 'http://127.0.0.1:5000';

async function apiService(endpoint, method = 'GET', body = null) {
  const headers = { 'Content-Type': 'application/json' };
  const config = {
    method,
    headers,
    body: body ? JSON.stringify(body) : null,
  };

  const response = await fetch(`${API_BASE_URL}${endpoint}`, config);

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({ message: 'Erro desconhecido no servidor' }));

    let errorMessage = errorData.message || `HTTP error! status: ${response.status}`;
    if (errorData.errors) {
        // Formata os erros de validação do Marshmallow para serem mais legíveis.
        const errorDetails = Object.entries(errorData.errors)
            .map(([field, messages]) => `- ${field}: ${messages.join(', ')}`)
            .join('\n');
        errorMessage += `\n\nDetalhes:\n${errorDetails}`;
    }
    throw new Error(errorMessage);
  }

  if (response.status === 204) { 
    return;
  }
  
  return response.json();
}

export const getInstitutionsByUf = (uf) => apiService(`/instituicoes?uf=${uf}`);
export const createInstitution = (data) => apiService('/instituicoes', 'POST', data);
export const updateInstitution = (id, ano, data) => apiService(`/instituicoes/${id}/${ano}`, 'PUT', data);
export const deleteInstitution = (id, ano) => apiService(`/instituicoes/${id}/${ano}`, 'DELETE');