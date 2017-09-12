
import { getNodes, getHistory } from './api';

export const initialState = {
    loading: true,
    nodes: null,
    nodesHistory: {},
    error: null,
};

export function fetchNodes() {
    return () => async dispatch => {
        try {
            const nodes = await getNodes();
            dispatch(state => ({
                ...state,
                loading: false,
                nodes,
            }));
        } catch (error) {
            console.error(error);
            dispatch(state => ({
                ...state,
                loading: false,
                error: error.toString(),
            }));
        }
    };
}

export function fetchHistory(node) {
    return () => async dispatch => {
        try {
            const history = await getHistory(node);
            dispatch(state => ({
                ...state,
                nodesHistory: {
                    ...state.nodesHistory,
                    [node]: history,
                },
            }));
        } catch (error) {
            console.error(error);
            dispatch(state => ({
                ...state,
                error: error.toString(),
            }));
        }
    };
}
