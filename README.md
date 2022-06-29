# Token supply

Collection of script to calculate token metrics for KINT and INTR.
Data source for these is Subscan.

- KINT: https://kintsugi.api.subscan.io/
- INTR: https://interlay.api.subscan.io/

### Deployment
The API is using [Flask](https://palletsprojects.com/p/flask/) to expose REST API.
It is hosted as [serverless Vercel function](https://vercel.com/docs/concepts/functions) inside the Interbtc-UI project [here](https://github.com/interlay/interbtc-ui/tree/master/api)