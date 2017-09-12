
import axios from 'axios';
import parse from 'date-fns/parse';

export const getNodes = async () => {
    const response = await axios.get('/nodes');
    return response.data.nodes;
};

export const getHistory = async (node) => {
    const response = await axios.get(`/node/${node}/history`);
    return response.data.entries.map(
        entry => ({
            ...entry,
            datetime: parse(entry.datetime),
        })
    );
};

export const getCurrent = async (node) => {
    const response = await axios.get(`/node/${node}/current`);
    return response.data;
};
