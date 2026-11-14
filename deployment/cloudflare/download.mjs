import archive from './download-manifest.json';
import {createDownloadWorker} from './zip-download.mjs';

export default createDownloadWorker(archive);
