import {initConnection, AverageSentiment} from "@/services/mongodb";
import {AgGridReactWrapper} from "@/components/AgGridReactWrapper";

const columnDefs = [{field: "ticker"}, {field: "occurrences"}, {field: "compound sentiment"}, {field: "price change 5D"}]

const fetchData = async (sentiment: any) => {
    const res = await fetch(`https://financialmodelingprep.com/api/v3/stock-price-change/${sentiment.ticker}?apikey=${process.env.FMP_API_KEY}`);
    const data = await res.json();
    return {
        ticker: sentiment.ticker,
        occurrences: sentiment.averageSentiment.count,
        'compound sentiment': sentiment.averageSentiment.compound.toFixed(3),
        'price change 5D': `${data[0]['5D']}%`
    };
};


export default async function Home() {
    initConnection();
    const averageSentiments = await AverageSentiment.find({}).sort({'averageSentiment.count': -1}).limit(15).exec();
    const promises = averageSentiments.map(fetchData);
    const rowData = await Promise.all(promises)

    return (
        <main>
            <h1 className="text-4xl font-semibold">Reddit Stocks Trend Analysis</h1>
            <div
                className="ag-theme-alpine"
                style={{height: '600px'}}
            >
                <AgGridReactWrapper
                    rowData={rowData}
                    columnDefs={columnDefs}
                ></AgGridReactWrapper>
            </div>
        </main>
    );
}

