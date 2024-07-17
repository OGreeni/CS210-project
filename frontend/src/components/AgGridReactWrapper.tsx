'use client'
import {FC} from 'react';
import {AgGridReact, AgGridReactProps} from "ag-grid-react";

interface AgGridReactWrapperProps extends AgGridReactProps {
}

export const AgGridReactWrapper: FC<AgGridReactWrapperProps> = (props) => <AgGridReact {...props} />;

