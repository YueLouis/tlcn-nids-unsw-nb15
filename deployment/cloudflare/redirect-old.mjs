// Keep links from the first Cloudflare handoff useful after the group chose ATTQ.
export default {
  fetch(request) {
    const destination = new URL(request.url);
    destination.protocol = 'https:';
    destination.host = 'attq-nids.phttrongtin-nguyen-a46.workers.dev';
    return Response.redirect(destination.href, 302);
  },
};
