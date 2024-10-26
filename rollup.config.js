import typescript from "@rollup/plugin-typescript"
import glob from "glob"
import * as path from "path"

// Find all page.ts files in the project
// Assumes that page.ts files are in a folder namespaced by the page name
const entryPoints = glob.sync("**/page.ts").map((file) => {
  const { dir } = path.parse(file)
  const pagesParentDir = path.dirname(dir)
  const pageDir = path.basename(dir)
  const builtFilePath = path.join(
    pagesParentDir,
    "built",
    pageDir + ".js"
  )
  return [file, builtFilePath]
})

const plugins = [typescript()]

const rollupConfig = entryPoints.map(([inputFilePath, outputFilePath]) => {
  return {
    input: inputFilePath,
    output: {
      file: outputFilePath,
      format: "cjs",
      sourcemap: true,
    },
    plugins,
  }
})

export default rollupConfig
