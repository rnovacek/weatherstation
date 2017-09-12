import Store, { thunk } from 'repatch';
import * as api from './api';
import { initialState } from './actions';

export default new Store(initialState).addMiddleware(thunk.withExtraArgument(api));
