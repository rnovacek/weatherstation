import React from 'react';
import PropTypes from 'prop-types';
import { CartesianGrid, Legend, Line, LineChart, Tooltip, XAxis, YAxis, ResponsiveContainer } from 'recharts';
import format from 'date-fns/format';
import startOfDay from 'date-fns/start_of_day';

import appStyle from '../style';

const formatTemperature = temp => `${Math.round(temp, 1)} C`;

const WeatherChart = ({ history }) => {
    const binSize = 10 * 60 * 1000;
    const aggregated = [];
    const ticks = [];
    let lastBin = null;
    let temperature = 0;
    let humidity = 0;
    let battery = 0;
    let count = 0;
    let minDate = Math.round(Date.now() / binSize);
    let maxDate = minDate;
    if (history) {
        history.forEach(
            (entry) => {
                const bin = Math.round(entry.datetime.valueOf() / binSize);
                if (lastBin && bin !== lastBin) {
                    aggregated.push({
                        temperature: temperature / count,
                        humidity: humidity / count,
                        battery: battery / count,
                        datetimeBin: bin,
                    });
                    temperature = 0;
                    humidity = 0;
                    battery = 0;
                    count = 0;
                    lastBin = bin;
                }
                temperature += entry.temperature;
                humidity += entry.humidity;
                battery += entry.battery;
                count += 1;
                if (!lastBin) {
                    lastBin = bin;
                }
            },
        );
        minDate = Math.round(history[0].datetime.valueOf() / binSize);
        maxDate = Math.round(history[history.length - 1].datetime.valueOf() / binSize);

        let d = startOfDay(history[0].datetime).valueOf() / binSize;
        while (d < maxDate) {
            if (d >= minDate) {
                ticks.push(d);
            }
            d += 12;
        }
    }

    const timeFormatter = (datetimeBin) => {
        const d = new Date(datetimeBin * binSize);
        if (d.getHours() === 0) {
            return format(d, 'D. M.');
        }
        return format(d, 'HH:mm');
    };
    const dateFormatter = (datetimeBin) => format(new Date(datetimeBin * binSize), 'YYYY-MM-DD HH:mm');

    const tooltipFormatter = (value, field) => {
        if (field === 'temperature') {
            return <span>{value.toFixed(1)}&deg;C</span>;
        }
        return <span>{value.toFixed(1)}&nbsp;%</span>;
    };

    return (
        <ResponsiveContainer aspect={3} >
            <LineChart width={300} height={100} data={aggregated}
                margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
                <XAxis
                    dataKey="datetimeBin"
                    type="number"
                    domain={[ticks[0], maxDate]}
                    ticks={ticks}
                    tickFormatter={timeFormatter}
                />

                <YAxis
                    yAxisId="left" orientation="left"
                    tickFormatter={formatTemperature}
                    tick={{ fill: '#637381' }}
                />
                <YAxis
                    yAxisId="right" orientation="right"
                />
                <CartesianGrid
                    strokeDasharray="3 3"
                    stroke="#666"
                />
                <Tooltip
                    labelFormatter={dateFormatter}
                    formatter={tooltipFormatter}
                />
                <Legend />
                <Line
                    yAxisId="left"
                    type="monotone"
                    dot={false}
                    dataKey="temperature"
                    stroke={appStyle.temperatureColor}
                />
                <Line
                    yAxisId="right"
                    type="monotone"
                    dot={false}
                    dataKey="humidity"
                    stroke={appStyle.humidityColor}
                />
                <Line
                    yAxisId="right"
                    type="monotone"
                    dot={false}
                    dataKey="battery"
                    stroke={appStyle.batteryColor}
                />
            </LineChart>
        </ResponsiveContainer>
    );
};

WeatherChart.propTypes = {
    history: PropTypes.arrayOf(
        PropTypes.shape({
            temperature: PropTypes.number.isRequired,
            humidity: PropTypes.number.isRequired,
            battery: PropTypes.number.isRequired,
            datetime: PropTypes.instanceOf(Date).isRequired,
        }).isRequired,
    ),
};

export default WeatherChart;
