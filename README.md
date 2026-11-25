<h1 align="center">[WIP] Create animation from trk</h1>

<p align="center">
  Work-in-progress utility that renders an animation of .trk streamlines over FreeSurfer cortical surfaces with Blender and outputs the rendered PNG frames.
</p>

<p align="center">
  <a href="https://github.com/brainlife/abcd-spec"><img src="https://img.shields.io/badge/ABCD_Spec-v1.1-green.svg" alt="ABCD Spec v1.1"></a>
  <a href="https://doi.org/10.25663/brainlife.app.526"><img src="https://img.shields.io/badge/Brainlife-brainlife.app.526-blue.svg" alt="Run on brainlife.io"></a>
</p>

## At a glance

<!-- brainlife-app:begin (generated from the App manifest; edit the manifest, not this block) -->

> **Work-in-progress utility that renders an animation of .trk streamlines over FreeSurfer cortical surfaces with Blender and outputs the rendered PNG frames.**

Converts the FreeSurfer lh/rh orig.nofix surfaces to STL with mris_convert, then renders 720 1920x1080 frames of the streamlines and surfaces with Blender 2.82. Marked work in progress; the frames are not assembled into a movie (the ffmpeg step is commented out). Needs a GPU.

| | |
|---|---|
| **Inputs** | `neuro/track/trk` · `neuro/freesurfer` |
| **Outputs** | `raw` |
| **Container** | `brainlife/freesurfer-mini:7.1.1` |
| **Requires** | `FREESURFER_LICENSE` |
| **Run it** | [doi.org/10.25663/brainlife.app.526](https://doi.org/10.25663/brainlife.app.526) |

#### Inputs

| Input | Datatype | Required | Description |
|---|---|---|---|
| `trk` | `neuro/track/trk` | yes | Tractogram (.trk) to animate. |
| `freesurfer` | `neuro/freesurfer` | yes | FreeSurfer subject directory providing the cortical surfaces. |

#### Outputs

| Output | Datatype | Description |
|---|---|---|
| `output` | `raw` | Rendered animation frames (frame.N.png). |

<!-- brainlife-app:end -->

## Running the App

### On brainlife.io

Open the App at [doi.org/10.25663/brainlife.app.526](https://doi.org/10.25663/brainlife.app.526), choose `neuro/track/trk`, `neuro/freesurfer` from your project and press **Execute**. The results are saved to your project as `raw`.

### Locally

You need [Singularity/Apptainer](https://apptainer.org/) (the App runs in `brainlife/freesurfer-mini:7.1.1`), [`jq`](https://jqlang.github.io/jq/), `FREESURFER_LICENSE`.

1. Clone this repository.
2. Create `config.json` with the paths to your inputs and the parameters:

   ```json
   {
       "track": "/path/to/trk/track",
       "freesurfer": "/path/to/freesurfer/freesurfer"
   }
   ```

3. Run `./main`.

## Troubleshooting

- **Please set FREESURFER_LICENSE in .bashrc**: Provide a FreeSurfer license (FREESURFER_LICENSE).

## Citing

If you use this App, please cite it, the software it builds on and brainlife.io:

- [WIP] Create animation from trk. brainlife.io App. [doi:10.25663/brainlife.app.526](https://doi.org/10.25663/brainlife.app.526)
- Fischl. FreeSurfer. *NeuroImage* 62:774-781 (2012). [doi:10.1016/j.neuroimage.2012.01.021](https://doi.org/10.1016/j.neuroimage.2012.01.021)
- Hayashi S, Caron BA, Heinsfeld AS, et al. brainlife.io: a decentralized and open-source cloud platform to support neuroscience research. *Nature Methods* 21:809–813 (2024). [doi:10.1038/s41592-024-02237-2](https://doi.org/10.1038/s41592-024-02237-2)
- Avesani P, McPherson B, Hayashi S, et al. The open diffusion data derivatives, brain data upcycling via integrated publishing of derivatives and reproducible open cloud services. *Scientific Data* 6:69 (2019). [doi:10.1038/s41597-019-0073-y](https://doi.org/10.1038/s41597-019-0073-y)

## Authors

Maintained by [@soichih](https://github.com/soichih).
