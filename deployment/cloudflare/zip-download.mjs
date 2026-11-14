// Join prevalidated static chunks using streaming rather than holding the ZIP in memory.
export function createDownloadWorker(archive) {
  return {
    async fetch(request, env) {
      const url = new URL(request.url);
      if (url.pathname !== archive.path) return env.ASSETS.fetch(request);
      if (!['GET', 'HEAD'].includes(request.method)) {
        return new Response('Method not allowed', {status: 405, headers: {Allow: 'GET, HEAD'}});
      }
      const headers = {
        'Content-Type': 'application/zip',
        'Content-Disposition': `attachment; filename="${archive.filename}"`,
        'Content-Length': String(archive.bytes),
        'Cache-Control': 'no-cache',
        'ETag': `"${archive.sha256}"`,
        'X-Content-Type-Options': 'nosniff',
      };
      if (request.method === 'HEAD') return new Response(null, {headers});
      let part = 0, reader;
      const body = new ReadableStream({
        async pull(controller) {
          try {
            for (;;) {
              if (!reader) {
                if (part === archive.parts.length) { controller.close(); return; }
                const response = await env.ASSETS.fetch(new Request(new URL(archive.parts[part++].path, request.url)));
                if (!response.ok || !response.body) throw new Error('Offline archive part unavailable');
                reader = response.body.getReader();
              }
              const chunk = await reader.read();
              if (chunk.done) { reader.releaseLock(); reader = undefined; continue; }
              controller.enqueue(chunk.value);
              return;
            }
          } catch (error) {
            await reader?.cancel(error);
            controller.error(error);
          }
        },
        async cancel(reason) { await reader?.cancel(reason); },
      });
      return new Response(body, {headers});
    },
  };
}
