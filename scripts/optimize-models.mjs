import { NodeIO } from '@gltf-transform/core';
import { ALL_EXTENSIONS } from '@gltf-transform/extensions';
import { dedup, prune, weld, simplify, textureCompress, meshopt } from '@gltf-transform/functions';
import { MeshoptEncoder, MeshoptDecoder, MeshoptSimplifier } from 'meshoptimizer';
import sharp from 'sharp';
import { stat, writeFile } from 'node:fs/promises';

await Promise.all([MeshoptEncoder.ready, MeshoptDecoder.ready, MeshoptSimplifier.ready]);
const io = new NodeIO().registerExtensions(ALL_EXTENSIONS).registerDependencies({
  'meshopt.encoder': MeshoptEncoder, 'meshopt.decoder': MeshoptDecoder,
});
const report = [];
for (const name of ['bandeja-v2.glb', 'coxinha.glb']) {
  const source = `model-sources/${name}`;
  const destination = `public/models/${name}`;
  const document = await io.read(source);
  const stats = () => document.getRoot().listMeshes().flatMap(mesh => mesh.listPrimitives()).reduce((sum, primitive) => sum + primitive.getIndices().getCount() / 3, 0);
  const trianglesBefore = stats();
  // Match the live matte material; this texture is unused by the site's renderer.
  document.getRoot().listMaterials().forEach(material => material.setMetallicRoughnessTexture(null).setMetallicFactor(0).setRoughnessFactor(.96));
  await document.transform(
    dedup(), prune(), weld(),
    simplify({ simplifier: MeshoptSimplifier, ratio: .5, error: .0005 }),
    textureCompress({ encoder: sharp, targetFormat: 'webp', slots: /baseColorTexture/, resize: [2048, 2048], quality: 88, effort: 80 }),
    textureCompress({ encoder: sharp, targetFormat: 'webp', slots: /normalTexture/, resize: [1024, 1024], lossless: true, effort: 80 }),
    prune(),
    meshopt({ encoder: MeshoptEncoder, level: 'high' }),
  );
  await io.write(destination, document);
  // Read compressed output again to verify buffers, extensions and texture data.
  const verified = await io.read(destination);
  if (!verified.getRoot().listMeshes().length || verified.getRoot().listTextures().length !== 2) throw new Error(`Invalid output: ${name}`);
  report.push({ name, originalBytes: (await stat(source)).size, optimizedBytes: (await stat(destination)).size, trianglesBefore, trianglesAfter: stats(), textures: verified.getRoot().listTextures().map(t => ({ format: t.getMimeType(), size: t.getSize() })) });
}
await writeFile('pesquisa/model-optimization.json', JSON.stringify(report, null, 2) + '\n');
console.log(JSON.stringify(report, null, 2));
