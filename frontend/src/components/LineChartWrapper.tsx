'use client'
import {LineChart, LineChartProps} from "@mui/x-charts";
import {FC} from 'react'

interface LineChartWrapperProps extends LineChartProps {
}

export const LineChartWrapper: FC<LineChartWrapperProps> = (props) => <LineChart {...props} />
