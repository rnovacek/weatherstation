import React, { Component } from 'react';
import { StyleRoot, Style } from 'radium';
import { Provider } from 'react-redux';
import store from '../store';

import WeatherApp from './WeatherApp';

class App extends Component {
    render() {
        return (
            <Provider store={store}>
                <StyleRoot>
                    <Style rules={{
                        body: {
                            fontFamily: 'Roboto,Helvetica Neue,Helvetica,Arial,sans-serif',
                            fontSize: '14px',
                            lineHeight: 1.5,
                            color: '#CFD2DA',
                            backgroundColor: '#252830',
                        }
                    }} />
                    <WeatherApp />
                </StyleRoot>
            </Provider>
        );
    }
}

export default App;
