import collections

from openstack_samplers import (
    CPUSampler,
    RAMSampler,
    IPSampler,
    RegionsRAMSampler,
    RegionsCPUSampler,
    RegionIPSampler,
    NagiosSampler,
    NagiosRegionSampler,
    ResourceSampler,
    # ConvergenceSampler,
)


def run(args, conf, app, xyzzy):

    client_cache = {}
    response_cache = {'x': 0, 'items': collections.deque()}

    samplers = [
        CPUSampler(xyzzy, 60, conf['openstack'], client_cache, response_cache),
        RAMSampler(xyzzy, 60, conf['openstack'], client_cache, response_cache),
        IPSampler(xyzzy, 60, conf['openstack'], client_cache, response_cache),
        RegionsCPUSampler(xyzzy, 60, conf['openstack'], client_cache,
                          response_cache),
        RegionsRAMSampler(xyzzy, 60, conf['openstack'], client_cache,
                          response_cache),
        RegionIPSampler(xyzzy, 60, conf['openstack'], client_cache,
                        response_cache),
        NagiosSampler(xyzzy, 15, conf['nagios']),
        NagiosRegionSampler(xyzzy, 15, conf['nagios']),
        ResourceSampler(xyzzy, 60, conf['openstack'], client_cache,
                        response_cache),
        # ConvergenceSampler(xyzzy, 1),
    ]

    try:
        app.run(debug=True,
                host=args.ip,
                port=args.port,
                threaded=True,
                use_reloader=False,
                use_debugger=True
                )
    finally:
        print "Disconnecting clients"
        xyzzy.stopped = True

        print "Stopping %d timers" % len(samplers)
        for (i, sampler) in enumerate(samplers):
            sampler.stop()

    print "Done"
