## crane registry
### Options
~~~
  -h, --help   help for registry
~~~
### Options inherited from parent commands
~~~
      --allow-nondistributable-artifacts   Allow pushing non-distributable (foreign) layers
      --insecure                           Allow image references to be fetched without TLS
      --platform platform                  Specifies the platform in the form os/arch[/variant][:osversion] (e.g. linux/amd64). (default all)
  -v, --verbose                            Enable debug logs
~~~
### SEE ALSO
* [crane](crane.md)	 - Crane is a tool for managing container images
* [crane registry serve](crane_registry_serve.md)	 - Serve a registry implementation
## crane tag
Efficiently tag a remote image
### Synopsis
Tag remote image without downloading it.

This differs slightly from the "copy" command in a couple subtle ways:

1. You don't have to specify the entire repository for the tag you're adding. For example, these two commands are functionally equivalent:
~~~
crane cp registry.example.com/library/ubuntu:v0 registry.example.com/library/ubuntu:v1
crane tag registry.example.com/library/ubuntu:v0 v1
~~~

2. We can skip layer existence checks because we know the manifest already exists. This makes "tag" slightly faster than "copy".
~~~
crane tag IMG TAG [flags]
~~~
### Examples
~~~
# Add a v1 tag to ubuntu
crane tag ubuntu v1
~~~
### Options
~~~
  -h, --help   help for tag
~~~
### Options inherited from parent commands
~~~
      --allow-nondistributable-artifacts   Allow pushing non-distributable (foreign) layers
      --insecure                           Allow image references to be fetched without TLS
      --platform platform                  Specifies the platform in the form os/arch[/variant][:osversion] (e.g. linux/amd64). (default all)
  -v, --verbose                            Enable debug logs
~~~
### SEE ALSO
* [crane](crane.md)	 - Crane is a tool for managing container images
## crane validate
Validate that an image is well-formed
~~~
crane validate [flags]
~~~
### Options
~~~
      --fast             Skip downloading/digesting layers
  -h, --help             help for validate
      --remote string    Name of remote image to validate
      --tarball string   Path to tarball to validate
~~~
### Options inherited from parent commands
~~~
      --allow-nondistributable-artifacts   Allow pushing non-distributable (foreign) layers
      --insecure                           Allow image references to be fetched without TLS
      --platform platform                  Specifies the platform in the form os/arch[/variant][:osversion] (e.g. linux/amd64). (default all)
  -v, --verbose                            Enable debug logs
~~~
### SEE ALSO
* [crane](crane.md)	 - Crane is a tool for managing container images
## crane version
Print the version
### Synopsis
The version string is completely dependent on how the binary was built, so you should not depend on the version format. It may change without notice.

This could be an arbitrary string, if specified via -ldflags.
This could also be the go module version, if built with go modules (often "(devel)").
~~~
crane version [flags]
~~~
### Options
~~~
  -h, --help   help for version
~~~
### Options inherited from parent commands
~~~
      --allow-nondistributable-artifacts   Allow pushing non-distributable (foreign) layers
      --insecure                           Allow image references to be fetched without TLS
      --platform platform                  Specifies the platform in the form os/arch[/variant][:osversion] (e.g. linux/amd64). (default all)
  -v, --verbose                            Enable debug logs
~~~
### SEE ALSO
* [crane](crane.md)	 - Crane is a tool for managing container images
## crane
Crane is a tool for managing container images
~~~
crane [flags]
~~~
### Options
~~~
      --allow-nondistributable-artifacts   Allow pushing non-distributable (foreign) layers
  -h, --help                               help for crane
      --insecure                           Allow image references to be fetched without TLS
      --platform platform                  Specifies the platform in the form os/arch[/variant][:osversion] (e.g. linux/amd64). (default all)
  -v, --verbose                            Enable debug logs
~~~
### SEE ALSO
* [crane append](crane_append.md)	 - Append contents of a tarball to a remote image
* [crane auth](crane_auth.md)	 - Log in or access credentials
* [crane blob](crane_blob.md)	 - Read a blob from the registry
* [crane catalog](crane_catalog.md)	 - List the repos in a registry
* [crane config](crane_config.md)	 - Get the config of an image
* [crane copy](crane_copy.md)	 - Efficiently copy a remote image from src to dst while retaining the digest value
* [crane delete](crane_delete.md)	 - Delete an image reference from its registry
* [crane digest](crane_digest.md)	 - Get the digest of an image
* [crane export](crane_export.md)	 - Export filesystem of a container image as a tarball
* [crane flatten](crane_flatten.md)	 - Flatten an image's layers into a single layer
* [crane index](crane_index.md)	 - Modify an image index.
* [crane ls](crane_ls.md)	 - List the tags in a repo
* [crane manifest](crane_manifest.md)	 - Get the manifest of an image
* [crane mutate](crane_mutate.md)	 - Modify image labels and annotations. The container must be pushed to a registry, and the manifest is updated there.
* [crane pull](crane_pull.md)	 - Pull remote images by reference and store their contents locally
* [crane push](crane_push.md)	 - Push local image contents to a remote registry
* [crane rebase](crane_rebase.md)	 - Rebase an image onto a new base image
* [crane registry](crane_registry.md)	 -
* [crane tag](crane_tag.md)	 - Efficiently tag a remote image
* [crane validate](crane_validate.md)	 - Validate that an image is well-formed
* [crane version](crane_version.md)	 - Print the version
## crane manifest
Get the manifest of an image
~~~
crane manifest IMAGE [flags]
~~~
### Options
~~~
  -h, --help   help for manifest
~~~
### Options inherited from parent commands
~~~
      --allow-nondistributable-artifacts   Allow pushing non-distributable (foreign) layers
      --insecure                           Allow image references to be fetched without TLS
      --platform platform                  Specifies the platform in the form os/arch[/variant][:osversion] (e.g. linux/amd64). (default all)
  -v, --verbose                            Enable debug logs
~~~
### SEE ALSO
* [crane](crane.md)	 - Crane is a tool for managing container images
## crane mutate
Modify image labels and annotations. The container must be pushed to a registry, and the manifest is updated there.
~~~
crane mutate [flags]
~~~
### Options
~~~
  -a, --annotation stringToString   New annotations to add (default [])
      --append strings              Path to tarball to append to image
      --cmd strings                 New cmd to set
      --entrypoint strings          New entrypoint to set
  -e, --env keyToValue              New envvar to add
      --exposed-ports strings       New ports to expose
  -h, --help                        help for mutate
  -l, --label stringToString        New labels to add (default [])
  -o, --output string               Path to new tarball of resulting image
      --repo string                 Repository to push the mutated image to. If provided, push by digest to this repository.
      --set-platform string         New platform to set in the form os/arch[/variant][:osversion] (e.g. linux/amd64)
  -t, --tag string                  New tag reference to apply to mutated image. If not provided, push by digest to the original image repository.
  -u, --user string                 New user to set
  -w, --workdir string              New working dir to set
~~~
### Options inherited from parent commands
~~~
      --allow-nondistributable-artifacts   Allow pushing non-distributable (foreign) layers
      --insecure                           Allow image references to be fetched without TLS
      --platform platform                  Specifies the platform in the form os/arch[/variant][:osversion] (e.g. linux/amd64). (default all)
  -v, --verbose                            Enable debug logs
~~~
### SEE ALSO
* [crane](crane.md)	 - Crane is a tool for managing container images
## crane pull
Pull remote images by reference and store their contents locally
~~~
crane pull IMAGE TARBALL [flags]
~~~
### Options
~~~
      --annotate-ref        Preserves image reference used to pull as an annotation when used with --format=oci
  -c, --cache_path string   Path to cache image layers
      --format string       Format in which to save images ("tarball", "legacy", or "oci") (default "tarball")
  -h, --help                help for pull
~~~
### Options inherited from parent commands
~~~
      --allow-nondistributable-artifacts   Allow pushing non-distributable (foreign) layers
      --insecure                           Allow image references to be fetched without TLS
      --platform platform                  Specifies the platform in the form os/arch[/variant][:osversion] (e.g. linux/amd64). (default all)
  -v, --verbose                            Enable debug logs
~~~
### SEE ALSO
* [crane](crane.md)	 - Crane is a tool for managing container images
## crane push
Push local image contents to a remote registry
### Synopsis
If the PATH is a directory, it will be read as an OCI image layout. Otherwise, PATH is assumed to be a docker-style tarball.
~~~
crane push PATH IMAGE [flags]
~~~
### Options
~~~
  -h, --help                help for push
      --image-refs string   path to file where a list of the published image references will be written
      --index               push a collection of images as a single index, currently required if PATH contains multiple images
~~~
### Options inherited from parent commands
~~~
      --allow-nondistributable-artifacts   Allow pushing non-distributable (foreign) layers
      --insecure                           Allow image references to be fetched without TLS
      --platform platform                  Specifies the platform in the form os/arch[/variant][:osversion] (e.g. linux/amd64). (default all)
  -v, --verbose                            Enable debug logs
~~~
### SEE ALSO
* [crane](crane.md)	 - Crane is a tool for managing container images
## crane rebase
Rebase an image onto a new base image
~~~
crane rebase [flags]
~~~
### Options
~~~
  -h, --help              help for rebase
      --new_base string   New base image to insert
      --old_base string   Old base image to remove
      --original string   Original image to rebase (DEPRECATED: use positional arg instead)
      --rebased string    Tag to apply to rebased image (DEPRECATED: use --tag)
  -t, --tag string        Tag to apply to rebased image
~~~
### Options inherited from parent commands
~~~
      --allow-nondistributable-artifacts   Allow pushing non-distributable (foreign) layers
      --insecure                           Allow image references to be fetched without TLS
      --platform platform                  Specifies the platform in the form os/arch[/variant][:osversion] (e.g. linux/amd64). (default all)
  -v, --verbose                            Enable debug logs
~~~
### SEE ALSO
* [crane](crane.md)	 - Crane is a tool for managing container images
## crane registry serve
Serve a registry implementation
### Synopsis
This sub-command serves a registry implementation on an automatically chosen port (:0), $PORT or --address

The command blocks while the server accepts pushes and pulls.

Contents are can be stored in memory (when the process exits, pushed data is lost.), and disk (--disk).
~~~
crane registry serve [flags]
~~~
### Options
~~~
      --address string   Address to listen on
      --disk string      Path to a directory where blobs will be stored
  -h, --help             help for serve
~~~
### Options inherited from parent commands
~~~
      --allow-nondistributable-artifacts   Allow pushing non-distributable (foreign) layers
      --insecure                           Allow image references to be fetched without TLS
      --platform platform                  Specifies the platform in the form os/arch[/variant][:osversion] (e.g. linux/amd64). (default all)
  -v, --verbose                            Enable debug logs
~~~
### SEE ALSO
* [crane registry](crane_registry.md)	 -
## crane export
Export filesystem of a container image as a tarball
~~~
crane export IMAGE|- TARBALL|- [flags]
~~~
### Examples
~~~
  # Write tarball to stdout
  crane export ubuntu -

  # Write tarball to file
  crane export ubuntu ubuntu.tar

  # Read image from stdin
  crane export - ubuntu.tar
~~~
### Options
~~~
  -h, --help   help for export
~~~
### Options inherited from parent commands
~~~
      --allow-nondistributable-artifacts   Allow pushing non-distributable (foreign) layers
      --insecure                           Allow image references to be fetched without TLS
      --platform platform                  Specifies the platform in the form os/arch[/variant][:osversion] (e.g. linux/amd64). (default all)
  -v, --verbose                            Enable debug logs
~~~
### SEE ALSO
* [crane](crane.md)	 - Crane is a tool for managing container images
## crane flatten
Flatten an image's layers into a single layer
~~~
crane flatten [flags]
~~~
### Options
~~~
  -h, --help         help for flatten
  -t, --tag string   New tag to apply to flattened image. If not provided, push by digest to the original image repository.
~~~
### Options inherited from parent commands
~~~
      --allow-nondistributable-artifacts   Allow pushing non-distributable (foreign) layers
      --insecure                           Allow image references to be fetched without TLS
      --platform platform                  Specifies the platform in the form os/arch[/variant][:osversion] (e.g. linux/amd64). (default all)
  -v, --verbose                            Enable debug logs
~~~
### SEE ALSO
* [crane](crane.md)	 - Crane is a tool for managing container images
## crane index append
Append manifests to a remote index.
### Synopsis
This sub-command pushes an index based on an (optional) base index, with appended manifests.

The platform for appended manifests is inferred from the config file or omitted if that is infeasible.
~~~
crane index append [flags]
~~~
### Examples
~~~
 # Append a windows hello-world image to ubuntu, push to example.com/hello-world:weird
  crane index append ubuntu -m hello-world@sha256:87b9ca29151260634b95efb84d43b05335dc3ed36cc132e2b920dd1955342d20 -t example.com/hello-world:weird

  # Create an index from scratch for etcd.
  crane index append -m registry.k8s.io/etcd-amd64:3.4.9 -m registry.k8s.io/etcd-arm64:3.4.9 -t example.com/etcd
~~~
### Options
~~~
      --docker-empty-base   If true, empty base index will have Docker media types instead of OCI
      --flatten             If true, appending an index will append each of its children rather than the index itself (default true)
  -h, --help                help for append
  -m, --manifest strings    References to manifests to append to the base index
  -t, --tag string          Tag to apply to resulting image
~~~
### Options inherited from parent commands
~~~
      --allow-nondistributable-artifacts   Allow pushing non-distributable (foreign) layers
      --insecure                           Allow image references to be fetched without TLS
      --platform platform                  Specifies the platform in the form os/arch[/variant][:osversion] (e.g. linux/amd64). (default all)
  -v, --verbose                            Enable debug logs
~~~
### SEE ALSO
* [crane index](crane_index.md)	 - Modify an image index.
## crane index filter
Modifies a remote index by filtering based on platform.
~~~
crane index filter [flags]
~~~
### Examples
~~~
  # Filter out weird platforms from ubuntu, copy result to example.com/ubuntu
  crane index filter ubuntu --platform linux/amd64 --platform linux/arm64 -t example.com/ubuntu

  # Filter out any non-linux platforms, push to example.com/hello-world
  crane index filter hello-world --platform linux -t example.com/hello-world

  # Same as above, but in-place
  crane index filter example.com/hello-world:some-tag --platform linux
~~~
### Options
~~~
  -h, --help                   help for filter
      --platform platform(s)   Specifies the platform(s) to keep from base in the form os/arch[/variant][:osversion][,<platform>] (e.g. linux/amd64).
  -t, --tag string             Tag to apply to resulting image
~~~
### Options inherited from parent commands
~~~
      --allow-nondistributable-artifacts   Allow pushing non-distributable (foreign) layers
      --insecure                           Allow image references to be fetched without TLS
  -v, --verbose                            Enable debug logs
~~~
### SEE ALSO
* [crane index](crane_index.md)	 - Modify an image index.
## crane index
Modify an image index.
~~~
crane index [flags]
~~~
### Options
~~~
  -h, --help   help for index
~~~
### Options inherited from parent commands
~~~
      --allow-nondistributable-artifacts   Allow pushing non-distributable (foreign) layers
      --insecure                           Allow image references to be fetched without TLS
      --platform platform                  Specifies the platform in the form os/arch[/variant][:osversion] (e.g. linux/amd64). (default all)
  -v, --verbose                            Enable debug logs
~~~
### SEE ALSO
* [crane](crane.md)	 - Crane is a tool for managing container images
* [crane index append](crane_index_append.md)	 - Append manifests to a remote index.
* [crane index filter](crane_index_filter.md)	 - Modifies a remote index by filtering based on platform.
## crane ls
List the tags in a repo
~~~
crane ls REPO [flags]
~~~
### Options
~~~
      --full-ref           (Optional) if true, print the full image reference
  -h, --help               help for ls
  -O, --omit-digest-tags   (Optional), if true, omit digest tags (e.g., ':sha256-...')
~~~
### Options inherited from parent commands
~~~
      --allow-nondistributable-artifacts   Allow pushing non-distributable (foreign) layers
      --insecure                           Allow image references to be fetched without TLS
      --platform platform                  Specifies the platform in the form os/arch[/variant][:osversion] (e.g. linux/amd64). (default all)
  -v, --verbose                            Enable debug logs
~~~
### SEE ALSO
* [crane](crane.md)	 - Crane is a tool for managing container images
## crane blob
Read a blob from the registry
~~~
crane blob BLOB [flags]
~~~
### Examples
~~~
crane blob ubuntu@sha256:4c1d20cdee96111c8acf1858b62655a37ce81ae48648993542b7ac363ac5c0e5 > blob.tar.gz
~~~
### Options
~~~
  -h, --help   help for blob
~~~
### Options inherited from parent commands
~~~
      --allow-nondistributable-artifacts   Allow pushing non-distributable (foreign) layers
      --insecure                           Allow image references to be fetched without TLS
      --platform platform                  Specifies the platform in the form os/arch[/variant][:osversion] (e.g. linux/amd64). (default all)
  -v, --verbose                            Enable debug logs
~~~
### SEE ALSO
* [crane](crane.md)	 - Crane is a tool for managing container images
## crane catalog
List the repos in a registry
~~~
crane catalog REGISTRY [flags]
~~~
### Options
~~~
      --full-ref   (Optional) if true, print the full image reference
  -h, --help       help for catalog
~~~
### Options inherited from parent commands
~~~
      --allow-nondistributable-artifacts   Allow pushing non-distributable (foreign) layers
      --insecure                           Allow image references to be fetched without TLS
      --platform platform                  Specifies the platform in the form os/arch[/variant][:osversion] (e.g. linux/amd64). (default all)
  -v, --verbose                            Enable debug logs
~~~
### SEE ALSO
* [crane](crane.md)	 - Crane is a tool for managing container images
## crane config
Get the config of an image
~~~
crane config IMAGE [flags]
~~~
### Options
~~~
  -h, --help   help for config
~~~
### Options inherited from parent commands
~~~
      --allow-nondistributable-artifacts   Allow pushing non-distributable (foreign) layers
      --insecure                           Allow image references to be fetched without TLS
      --platform platform                  Specifies the platform in the form os/arch[/variant][:osversion] (e.g. linux/amd64). (default all)
  -v, --verbose                            Enable debug logs
~~~
### SEE ALSO
* [crane](crane.md)	 - Crane is a tool for managing container images
## crane copy
Efficiently copy a remote image from src to dst while retaining the digest value
~~~
crane copy SRC DST [flags]
~~~
### Options
~~~
  -a, --all-tags     (Optional) if true, copy all tags from SRC to DST
  -h, --help         help for copy
  -j, --jobs int     (Optional) The maximum number of concurrent copies, defaults to GOMAXPROCS
  -n, --no-clobber   (Optional) if true, avoid overwriting existing tags in DST
~~~
### Options inherited from parent commands
~~~
      --allow-nondistributable-artifacts   Allow pushing non-distributable (foreign) layers
      --insecure                           Allow image references to be fetched without TLS
      --platform platform                  Specifies the platform in the form os/arch[/variant][:osversion] (e.g. linux/amd64). (default all)
  -v, --verbose                            Enable debug logs
~~~
### SEE ALSO
* [crane](crane.md)	 - Crane is a tool for managing container images
## crane delete
Delete an image reference from its registry
~~~
crane delete IMAGE [flags]
~~~
### Options
~~~
  -h, --help   help for delete
~~~
### Options inherited from parent commands
~~~
      --allow-nondistributable-artifacts   Allow pushing non-distributable (foreign) layers
      --insecure                           Allow image references to be fetched without TLS
      --platform platform                  Specifies the platform in the form os/arch[/variant][:osversion] (e.g. linux/amd64). (default all)
  -v, --verbose                            Enable debug logs
~~~
### SEE ALSO
* [crane](crane.md)	 - Crane is a tool for managing container images
## crane digest
Get the digest of an image
~~~
crane digest IMAGE [flags]
~~~
### Options
~~~
      --full-ref         (Optional) if true, print the full image reference by digest
  -h, --help             help for digest
      --tarball string   (Optional) path to tarball containing the image
~~~
### Options inherited from parent commands
~~~
      --allow-nondistributable-artifacts   Allow pushing non-distributable (foreign) layers
      --insecure                           Allow image references to be fetched without TLS
      --platform platform                  Specifies the platform in the form os/arch[/variant][:osversion] (e.g. linux/amd64). (default all)
  -v, --verbose                            Enable debug logs
~~~
### SEE ALSO
* [crane](crane.md)	 - Crane is a tool for managing container images
## crane append
Append contents of a tarball to a remote image
### Synopsis
This sub-command pushes an image based on an (optional)
base image, with appended layers containing the contents of the
provided tarballs.

If the base image is a Windows base image (i.e., its config.OS is "windows"),
the contents of the tarballs will be modified to be suitable for a Windows
container image.
~~~
crane append [flags]
~~~
### Options
~~~
  -b, --base string                  Name of base image to append to
  -h, --help                         help for append
  -f, --new_layer strings            Path to tarball to append to image
  -t, --new_tag string               Tag to apply to resulting image
      --oci-empty-base               If true, empty base image will have OCI media types instead of Docker
  -o, --output string                Path to new tarball of resulting image
      --set-base-image-annotations   If true, annotate the resulting image as being based on the base image
~~~
### Options inherited from parent commands
~~~
      --allow-nondistributable-artifacts   Allow pushing non-distributable (foreign) layers
      --insecure                           Allow image references to be fetched without TLS
      --platform platform                  Specifies the platform in the form os/arch[/variant][:osversion] (e.g. linux/amd64). (default all)
  -v, --verbose                            Enable debug logs
~~~
### SEE ALSO
* [crane](crane.md)	 - Crane is a tool for managing container images
## crane auth get
Implements a credential helper
~~~
crane auth get [REGISTRY_ADDR] [flags]
~~~
### Examples
~~~
  # Read configured credentials for reg.example.com
  $ echo "reg.example.com" | crane auth get
  {"username":"AzureDiamond","password":"hunter2"}
  # or
  $ crane auth get reg.example.com
  {"username":"AzureDiamond","password":"hunter2"}
~~~
### Options
~~~
  -h, --help   help for get
~~~
### Options inherited from parent commands
~~~
      --allow-nondistributable-artifacts   Allow pushing non-distributable (foreign) layers
      --insecure                           Allow image references to be fetched without TLS
      --platform platform                  Specifies the platform in the form os/arch[/variant][:osversion] (e.g. linux/amd64). (default all)
  -v, --verbose                            Enable debug logs
~~~
### SEE ALSO
* [crane auth](crane_auth.md)	 - Log in or access credentials
## crane auth login
Log in to a registry
~~~
crane auth login [OPTIONS] [SERVER] [flags]
~~~
### Examples
~~~
  # Log in to reg.example.com
  crane auth login reg.example.com -u AzureDiamond -p hunter2
~~~
### Options
~~~
  -h, --help              help for login
  -p, --password string   Password
      --password-stdin    Take the password from stdin
  -u, --username string   Username
~~~
### Options inherited from parent commands
~~~
      --allow-nondistributable-artifacts   Allow pushing non-distributable (foreign) layers
      --insecure                           Allow image references to be fetched without TLS
      --platform platform                  Specifies the platform in the form os/arch[/variant][:osversion] (e.g. linux/amd64). (default all)
  -v, --verbose                            Enable debug logs
~~~
### SEE ALSO
* [crane auth](crane_auth.md)	 - Log in or access credentials
## crane auth logout
Log out of a registry
~~~
crane auth logout [SERVER] [flags]
~~~
### Examples
~~~
  # Log out of reg.example.com
  crane auth logout reg.example.com
~~~
### Options
~~~
  -h, --help   help for logout
~~~
### Options inherited from parent commands
~~~
      --allow-nondistributable-artifacts   Allow pushing non-distributable (foreign) layers
      --insecure                           Allow image references to be fetched without TLS
      --platform platform                  Specifies the platform in the form os/arch[/variant][:osversion] (e.g. linux/amd64). (default all)
  -v, --verbose                            Enable debug logs
~~~
### SEE ALSO
* [crane auth](crane_auth.md)	 - Log in or access credentials
## crane auth token
Retrieves a token for a remote repo
~~~
crane auth token REPO [flags]
~~~
### Examples
~~~
# If you wanted to mount a blob from debian to ubuntu.
$ curl -H "$(crane auth token -H --push --mount debian ubuntu)" ...

# To get the raw list tags response
$ curl -H "$(crane auth token -H ubuntu)" https://index.docker.io/v2/library/ubuntu/tags/list
~~~
### Options
~~~
  -H, --header          Output in header format
  -h, --help            help for token
  -m, --mount strings   Scopes to mount from
      --push            Request push scopes
~~~
### Options inherited from parent commands
~~~
      --allow-nondistributable-artifacts   Allow pushing non-distributable (foreign) layers
      --insecure                           Allow image references to be fetched without TLS
      --platform platform                  Specifies the platform in the form os/arch[/variant][:osversion] (e.g. linux/amd64). (default all)
  -v, --verbose                            Enable debug logs
~~~
### SEE ALSO
* [crane auth](crane_auth.md)	 - Log in or access credentials
## crane auth
Log in or access credentials
~~~
crane auth [flags]
~~~
### Options
~~~
  -h, --help   help for auth
~~~
### Options inherited from parent commands
~~~
      --allow-nondistributable-artifacts   Allow pushing non-distributable (foreign) layers
      --insecure                           Allow image references to be fetched without TLS
      --platform platform                  Specifies the platform in the form os/arch[/variant][:osversion] (e.g. linux/amd64). (default all)
  -v, --verbose                            Enable debug logs
~~~
### SEE ALSO
* [crane](crane.md)	 - Crane is a tool for managing container images
* [crane auth get](crane_auth_get.md)	 - Implements a credential helper
* [crane auth login](crane_auth_login.md)	 - Log in to a registry
* [crane auth logout](crane_auth_logout.md)	 - Log out of a registry
* [crane auth token](crane_auth_token.md)	 - Retrieves a token for a remote repo
