// Historical document URLs lead to restricted Drive without reading an asset.
export function createPublicDemoWorker(policy) {
  return {
    async fetch(request, env) {
      let path;
      try {
        path = decodeURIComponent(new URL(request.url).pathname).toLowerCase();
      } catch {
        return new Response('Invalid URL', {status: 400});
      }
      const retired = policy.retired_prefixes.some((prefix) => path === prefix || path.startsWith(prefix + '/'))
        || policy.private_extensions.some((extension) => path.endsWith(extension));
      if (!retired) return env.ASSETS.fetch(request);
      const headers = {
        'Cache-Control': 'no-store',
        'X-Content-Type-Options': 'nosniff',
        'X-Robots-Tag': 'noindex, nofollow',
      };
      if (!['GET', 'HEAD'].includes(request.method)) {
        return new Response('Method not allowed', {status: 405, headers: {...headers, Allow: 'GET, HEAD'}});
      }
      const location = path === '/assets/bao_cao_dot3.pdf' ? policy.round3_url : policy.reports_url;
      return new Response(null, {status: 302, headers: {...headers, Location: location}});
    },
  };
}
