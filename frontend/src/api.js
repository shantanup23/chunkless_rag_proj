import axios from 'axios';

const api = axios.create({
    baseURL: 'http://127.0.0.1:8002',
});

export const uploadFile = async (file) => {
    const formData = new FormData();
    formData.append('file', file);
    const response = await api.post('/api/upload', formData, {
        headers: {
            'Content-Type': 'multipart/form-data',
        },
    });
    return response.data;
};

export const generateTest = async (payload) => {
    const response = await api.post('/api/generate-test', payload);
    return response.data;
};
