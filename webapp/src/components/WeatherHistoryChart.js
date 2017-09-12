import React from 'react';
import PropTypes from 'prop-types';
import { connect } from 'react-redux';

import WeatherChart from './WeatherChart';
import { fetchHistory } from '../actions';

class WeatherHistoryChart extends React.Component {
    reloadInterval = null;

    componentDidMount() {
        this.reload();
        this.reloadInterval = setInterval(this.reload, 60 * 1000);
    }

    componentWillUnmount() {
        clearInterval(this.reloadInterval);
    }

    reload = () => {
        this.props.dispatch(fetchHistory(this.props.node));
    }

    render() {
        return (
            <WeatherChart
                history={this.props.history}
            />
        );
    }
}

WeatherHistoryChart.propTypes = {
    dispatch: PropTypes.func.isRequired,
    node: PropTypes.number.isRequired,
    history: PropTypes.array,
};

export default connect(
    (state, ownProps) => ({
        history: state.nodesHistory[ownProps.node],
    })
)(WeatherHistoryChart);
