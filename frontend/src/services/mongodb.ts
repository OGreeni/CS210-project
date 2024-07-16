import mongoose from 'mongoose'
import {Schema, model} from 'mongoose'

export const initConnection = () => {
    mongoose.connect(process.env.MONGODB_URI ?? "").catch(console.error)
}


const postSchema = new Schema({
    timestamp: Date,
    tickers: [String],
    sentiment: Number
})

const averageSentimentSchema = new Schema({
    ticker: String,
    averageSentiment: {
        compound: Number,
        pos: Number,
        neu: Number,
        neg: Number,
        count: Number
    }
})

// export const Post = model('posts', postSchema);
console.log(mongoose.models)

export const AverageSentiment = mongoose.models.average_sentiments || model('average_sentiments', averageSentimentSchema);
