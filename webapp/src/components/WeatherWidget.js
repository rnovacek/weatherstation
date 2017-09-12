import React from 'react';
import PropTypes from 'prop-types';
import Radium from 'radium';
import parse from 'date-fns/parse';
import distanceInWordsStrict from 'date-fns/distance_in_words_strict';

import WeatherValue from './WeatherValue';
import WeatherHistoryChart from './WeatherHistoryChart';
import { getCurrent } from '../api';
import appStyle from '../style';

const styles = {
    base: {
        display: 'flex',
        flexDirection: 'row',
        flexWrap: 'wrap',
        color: 'gray',
    },
    cell: {
        flexBasis: '25%',
        textAlign: 'center',
        fontVariant: 'small-caps',
    },
    temperature: {
        color: appStyle.temperatureColor,
        fontSize: '150%',
    },
    humidity: {
        color: appStyle.humidityColor,
        fontSize: '150%',
    },
    battery: {
        color: appStyle.batteryColor,
        fontSize: '150%',
    },
    row: {
        width: '100%',
        marginTop: '1em',
    },
};

class WeatherWidget extends React.Component {
    reloadInterval = null;
    updateInterval = null;
    state = {
        temperature: null,
        humidity: null,
        battery: null,
        lastUpdate: null,
        lastUpdateString: null,
    };

    componentDidMount() {
        this.reloadInterval = setInterval(this.loadAndUpdateData, 5000);
        this.updateInterval = setInterval(this.update, 1000);
        this.loadAndUpdateData();
    }

    componentWillUnmount() {
        clearInterval(this.updateInterval);
        clearInterval(this.reloadInterval);
    }

    loadAndUpdateData = async () => {
        const current = await getCurrent(this.props.node);
        this.setState({
            temperature: current.temperature,
            humidity: current.humidity,
            battery: current.battery,
            lastUpdate: parse(current.dt),
        });
        this.update();
    };

    update = () => {
        this.setState({
            lastUpdateString: distanceInWordsStrict(this.state.lastUpdate, new Date()),
        });
    };

    render() {
        return (
            <div style={[styles.base]}>
                <div style={[styles.cell]}>
                    <WeatherValue
                        title="Temperature"
                        value={this.state.temperature}
                        style={styles.temperature}
                        formatter={value => (value ? <span>{value.toFixed(1)}&deg;C</span> : '')}
                    />
                </div>
                <div style={[styles.cell]}>
                    <WeatherValue
                        title="Humidity"
                        value={this.state.humidity}
                        style={styles.humidity}
                        formatter={value => (value ? <span>{value.toFixed(1)}&nbsp;%</span> : '')}
                    />
                </div>
                <div style={[styles.cell]}>
                    <WeatherValue
                        title="Battery"
                        value={this.state.battery}
                        style={styles.battery}
                        formatter={value => (value ? <span>{value.toFixed(1)}&nbsp;%</span> : '')}
                    />
                </div>
                <div style={[styles.cell]}>
                    <WeatherValue
                        title="Last update"
                        value={this.state.lastUpdate}
                        formatter={value => (value ? `${distanceInWordsStrict(value, new Date())} ago` : '')}
                    />
                </div>
                <div style={[styles.row]}>
                    <WeatherHistoryChart node={this.props.node} />
                </div>
            </div>
        );
    }
}

WeatherWidget.propTypes = {
    node: PropTypes.number.isRequired,
};

export default Radium(WeatherWidget);
