# Open Higgsfield setup

[Open Higgsfield](https://github.com/Anil-matcha/Open-Higgsfield-AI) (now "Open Generative AI") is a
web UI over [MuAPI](https://muapi.ai), a paid hosted API. The UI is free; every generation costs
MuAPI credits and needs a MuAPI API key.

## Run the app

    ./setup.sh start     # clone, install, build, serve on http://localhost:3000

Paste your MuAPI key into the app's Settings. Needs Node 18+ and git.

## Generate videos without the UI

    cp prompts.example.json prompts.json   # edit prompts
    MUAPI_KEY=... node make_video.mjs prompts.json

MP4s land in `videos/`. Each job takes `prompt`, `model`, and whichever of `aspect_ratio`,
`duration`, `resolution`, `quality` the model supports. Model ids are the `id` values in
`app/packages/studio/src/models.js` (`t2vModels`), e.g. `seedance-lite-t2v`,
`kling-v2.5-turbo-pro-t2v`, `veo3.1-fast-text-to-video`, `wan2.2-text-to-video`.
