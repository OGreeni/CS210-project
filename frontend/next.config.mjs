const nextConfig = {
    experimental: {
        esmExternals: "loose", // <-- add this
        serverComponentsExternalPackages: ["mongoose"]
    },
    webpack: (config) => {
        config.experiments = {
            topLevelAwait: true
        };
        return config;
    },
}
