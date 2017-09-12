import React from 'react';
import PropTypes from 'prop-types';
import { connect } from 'react-redux';

import WeatherWidget from './WeatherWidget';
import { fetchNodes } from '../actions';

class WeatherApp extends React.Component {
    componentDidMount() {
        this.props.dispatch(fetchNodes());
    }

    render() {
        const { loading, nodes, error } = this.props;
        if (loading) {
            return <div>Loading</div>;
        }
        if (error) {
            return <div>{error.toString()}</div>;
        }
        return (
            <div>
                {
                    nodes.map(
                        node => (
                            <WeatherWidget key={node} node={node} />
                        ),
                    )
                }
            </div>
        );
    }
}

WeatherApp.propTypes = {
    dispatch: PropTypes.func.isRequired,
    loading: PropTypes.bool.isRequired,
    nodes: PropTypes.array,
    error: PropTypes.string,
};

export default connect(
    state => ({
        loading: state.loading,
        nodes: state.nodes,
        error: state.error,
    })
)(WeatherApp);
