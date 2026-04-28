import { defineConfig } from '@hey-api/openapi-ts';

export default defineConfig({
    input: 'https://raw.githubusercontent.com/SeerAPI/api-data/refs/heads/main/data/v1/openapi.json',
    output: {
        path: 'src/client',
    },
    plugins: [
        {
            dates: true,
            name: '@hey-api/transformers',
        },
        {
            examples: {
                moduleName: '@seerapi/client',
            },
            transformer: true,
            name: '@hey-api/sdk',
        },
        '@hey-api/client-axios',
    ]
});