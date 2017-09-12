import React from 'react';
import PropTypes from 'prop-types';
import Radium from 'radium';

const styles = {
    base: {
        display: 'flex',
        flexDirection: 'column',
    },
};

const WeatherValue = ({ title, value, formatter, style }) => {
    return (
        <div style={[styles.base]}>
            <div>{title}</div>
            <div style={style}>
                {
                    formatter ?
                        formatter(value)
                        :
                        value
                }
            </div>
        </div>
    );
};

WeatherValue.propTypes = {
    title: PropTypes.string.isRequired,
    value: PropTypes.any,
    formatter: PropTypes.func,
    style: PropTypes.object,
};

export default Radium(WeatherValue);
