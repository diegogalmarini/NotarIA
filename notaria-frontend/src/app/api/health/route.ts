import { NextResponse } from 'next/server'

export async function GET() {
  return NextResponse.json({ status: 'healthy', service: 'Tutor Ingesis API - Next', mode: 'serverless' })
}

export async function OPTIONS() {
  return new NextResponse(null, {
    headers: {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type, Authorization',
    },
  })
}
