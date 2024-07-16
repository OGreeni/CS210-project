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
        'price change 5D': `${data[0]['5D']}%`,
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

        // Push sentiment or any other value from the post into the corresponding bin
        groupedPosts[daysDifference].push(post.sentiment);
    });

    return groupedPosts.filter((group) => group !== undefined).reverse();
}


export default async function Home() {
    initConnection();
    const averageSentiments = await AverageSentiment.find({}).sort({'averageSentiment.count': -1}).exec();
    const promises = averageSentiments.map(fetchData);
    const rowData = await Promise.all(promises)

    const groupedPosts = await getGroupedPosts('TSLA');
    console.log(groupedPosts)

    return (
        <main>
            <h1 className="text-4xl font-semibold text-center">Reddit Stocks Trend Analysis</h1>
            <div
                className="ag-theme-alpine"
                style={{height: '600px', maxWidth: '1000px', marginInline: 'auto'}}
            >
                <AgGridReactWrapper
                    rowData={rowData}
                    columnDefs={columnDefs}
                ></AgGridReactWrapper>
            </div>
            <LineChartWrapper
                series={[
                    {
                        data: groupedPosts.map(group => group.reduce((a, b) => a + b) / group.length),
                        label: 'Sentiment'
                    },
                    {
                        data: groupedPosts.map(group => group.length),
                        label: 'Occurrences',
                    }
                ]}
                width={500}
                height={300}
                xAxis={[{
                    label: 'Days',
                    data: Array.from(groupedPosts.keys()),
                    tickNumber: Array.from(groupedPosts.keys()).length
                }]}
            />
        </main>
    );
}

