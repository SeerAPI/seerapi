import { existsSync } from 'node:fs';
import { defineConfig } from '@hey-api/openapi-ts';

const LOCAL_OPENAPI_PATH = '../../output/v1/openapi.json';
const REMOTE_OPENAPI_URL =
    'https://raw.githubusercontent.com/SeerAPI/api-data/refs/heads/main/data/v1/openapi.json';

function resolveInput(): string {
    if (process.env.OPENAPI_INPUT) return process.env.OPENAPI_INPUT;
    if (existsSync(LOCAL_OPENAPI_PATH)) return LOCAL_OPENAPI_PATH;
    return REMOTE_OPENAPI_URL;
}

export default defineConfig({
    input: resolveInput(),
    output: {
        path: 'src/client',
        module: {
            extension: '.js',
        },
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