import {LineChartWrapper} from "@/components/LineChartWrapper";
import {initConnection, AverageSentiment, Post} from "@/services/mongodb";
import {AgGridReactWrapper} from "@/components/AgGridReactWrapper";

const columnDefs = [{field: "ticker"}, {field: "occurrences"}, {field: "compound sentiment"}, {field: "price change 5D"}]

const fetchData = async (sentiment: any) => {
    const res = await fetch(`https://financialmodelingprep.com/api/v3/stock-price-change/${sentiment.ticker}?apikey=${process.env.FMP_API_KEY}`);
    const data = await res.json();
    return {
        ticker: sentiment.ticker,
        occurrences: sentiment.averageSentiment.count,
        'compound sentiment': sentiment.averageSentiment.compound.toFixed(3),
        'price change 5D': `${data[0]?.['5D']}%`,
    };
};

const getGroupedPosts = async (ticker: string) => {
    const ONE_DAY_MS = 24 * 60 * 60 * 1000; // Number of milliseconds in a day

    const posts = await Post.find({tickers: {$in: [ticker]}})
        .sort({timestamp: -1})
        .exec();

    // Get current timestamp in milliseconds
    const currentDate = new Date().getTime();

    // Initialize an object to store bins dynamically
    const groupedPosts: number[][] = [];

    // Group posts into bins based on their timestamp
    posts.forEach((post) => {
        const postTimestamp = post.timestamp.getTime() * 1000;

        // Calculate difference in days
        const daysDifference = Math.floor((currentDate - postTimestamp) / ONE_DAY_MS);

        // Initialize the bin array if it doesn't exist
        if (!groupedPosts[daysDifference]) {
            groupedPosts[daysDifference] = [];
        }

        // Push sentiment from the post into the corresponding bin
        groupedPosts[daysDifference].push(post.sentiment);
    });

    return {
        groupedPosts: groupedPosts,
        reducedGroupedPosts: groupedPosts.filter((group) => group !== undefined)
    };
}

const getStockPrices = async (ticker: string, groupedPosts: number[][]) => {
    const res = await fetch(`https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=${ticker}&apikey=${process.env.AV_API_KEY}`)
    const data = await res.json();

    const closePrices: number[] = [];

    for (let i = 0; i < groupedPosts.length; i++) {
        if (!groupedPosts[i]) {
            continue;
        }

        // Calculate target date
        const today = new Date();
        const targetDate = new Date(today);
        targetDate.setDate(today.getDate() - i);

        // Format target date to match API data key format (YYYY-MM-DD)
        const targetDateStr = targetDate.toISOString().slice(0, 10);

        if (data['Time Series (Daily)'][targetDateStr]) {
            const stockData = data['Time Series (Daily)'][targetDateStr];
            closePrices.push(parseFloat(stockData['4. close']));
        } else {
            closePrices.push(closePrices[closePrices.length - 1]);
        }
    }

    return closePrices;
}

// Function to find unique documents based on a property
function findUniqueByProperty(array: any, property: any) {
    const map = new Map();
    array.forEach((item: any) => {
        const key = item[property];
        if (!map.has(key)) {
            map.set(key, item);
        }
    });
    return Array.from(map.values());
}

export default async function Home() {
    initConnection();
    const averageSentiments = findUniqueByProperty(await AverageSentiment.find({}).sort({'averageSentiment.count': -1}).exec(), 'ticker');
    const promises = averageSentiments.map(fetchData);
    const rowData = await Promise.all(promises);


    const topAverageSentiments = averageSentiments.slice(0, 5);

    const results: any[] = [];

    await Promise.all(topAverageSentiments.map(async (sentiment) => {
        // Fetch data for the current sentiment
        const rowData = await fetchData(sentiment);

        // Get grouped posts for the current ticker
        const groupedPosts = await getGroupedPosts(sentiment.ticker);

        // Get stock prices for the current ticker using grouped posts
        const stockPrices = await getStockPrices(sentiment.ticker, groupedPosts.groupedPosts.reverse());

        // Push result object to results array
        results.push({
            ticker: sentiment.ticker,
            groupedPosts: groupedPosts,
            stockPrices: stockPrices
        });
    }));

    console.log(results);
    return (
        <main>
            <div className="h-10"/>
            <h1 className="text-4xl font-semibold text-center">Reddit Stocks Trend Analysis</h1>
            <div className="h-10"/>
            <div
                className="ag-theme-alpine"
                style={{height: '600px', maxWidth: '1000px', marginInline: 'auto'}}
            >
                <AgGridReactWrapper
                    rowData={rowData}
                    columnDefs={columnDefs}
                />
            </div>
            <div className="h-10"/>
            <div className="flex justify-center items-center flex-wrap">
                {results.map(result => <div className="justify-center items-center" key={result.ticker}>
                    <div className="text-center font-semibold text-xl">{result.ticker}</div>
                    <LineChartWrapper
                        series={[
                            {
                                data: result.groupedPosts.reducedGroupedPosts.reverse().map((group: any) => group.reduce((a: number, b: number) => a + b) / group.length),
                                label: 'Sentiment'
                            },
                            {
                                data: result.groupedPosts.reducedGroupedPosts.reverse().map((group: any) => group.length),
                                label: 'Occurrences',
                            },
                            {
                                data: result.stockPrices.map((stockPrice: number, i: number) => {
                                    if (i === 0) {
                                        return 0;
                                    } else {
                                        const prevPrice = result.stockPrices[i - 1];
                                        const percentChange = ((stockPrice - prevPrice) / prevPrice) * 100 || 0;
                                        return percentChange;
                                    }
                                }),
                                label: '% change in price'
                            }
                        ]}
                        width={500}
                        height={300}
                        xAxis={[{
                            label: 'Days',
                            data: Array.from(result.groupedPosts.reducedGroupedPosts.keys()),
                            tickNumber: Array.from(result.groupedPosts.reducedGroupedPosts.keys()).length
                        }]}
                    />
                </div>)}
            </div>
        </main>
    );
}

